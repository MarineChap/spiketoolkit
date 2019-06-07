"""
High level tools to run many groundtruth comparison with
many sorter on many recordings and then collect and aggregate results
in an easy way.

the all mechanism is based on an intrinsinct organisation
into a "study_folder" with several subfolder:
  * raw_files : contain a copy in binary format of recordings
  * sorter_outputs : contains output of sorters
  * ground_truth : contains a copy of sorting groun truth
"""

from pathlib import Path
import os
import json

import pandas as pd

import spikeextractors as se

from spiketoolkit.sorters import run_sorters, loop_over_folders, collect_sorting_outputs
from .groundtruthcomparison import compare_sorter_to_ground_truth, _perf_keys


def setup_comparison_study(study_folder, gt_dict):
    """
    Based on a dict of (recordnig, sorting) create the study folder.
    

    Parameters
    ----------
    study_folder: str
        The study folder.
    
    gt_dict : a dict of tuple (recording, sorting_gt)
        Dict of tuple that contain recording and sorting ground truth
    """
    
    study_folder = Path(study_folder)
    assert not os.path.exists(study_folder), 'study_folder already exists'
    
    os.makedirs(study_folder)
    os.makedirs(study_folder / 'raw_files')
    os.makedirs(study_folder / 'ground_truth')
    
    
    for rec_name, (recording, sorting_gt) in gt_dict.items():
        
        # write recording as binary format + json + prb
        raw_filename = study_folder / 'raw_files' / (rec_name+'.raw')
        prb_filename = study_folder / 'raw_files' / (rec_name+'.prb')
        json_filename = study_folder / 'raw_files' / (rec_name+'.json')
        num_chan = recording.get_num_channels()
        chunksize = 2**24// num_chan
        sr = recording.get_sampling_frequency()
        
        se.write_binary_dat_format(recording, raw_filename, time_axis=0, dtype='float32', chunksize=chunksize)
        se.save_probe_file(recording, prb_filename, format='spyking_circus')
        with open(json_filename, 'w', encoding='utf8') as f:
            info = dict(sample_rate=sr, num_chan=num_chan, dtype='float32', frames_first=True)
            json.dump(info, f, indent=4)
        
        # write recording sorting_gt as with npz format
        se.NpzSortingExtractor.write_sorting(sorting_gt, study_folder / 'ground_truth' / (rec_name+'.npz'))
    
    # make an index of recording names
    with open(study_folder / 'names.txt', mode='w', encoding='utf8') as f:
        for rec_name in  gt_dict:
            f.write(rec_name + '\n')


def get_rec_names(study_folder):
    with open(study_folder / 'names.txt', mode='r', encoding='utf8') as f:
        rec_names = f.read()[:-1].split('\n')
    return rec_names


def get_recordings(study_folder):
    study_folder = Path(study_folder)
    
    rec_names = get_rec_names(study_folder)
    recording_dict = {}
    for rec_name in rec_names:
        raw_filename = study_folder / 'raw_files' / (rec_name+'.raw')
        prb_filename = study_folder / 'raw_files' / (rec_name+'.prb')
        json_filename = study_folder / 'raw_files' / (rec_name+'.json')
        with open(json_filename, 'r', encoding='utf8') as f:
            info = json.load(f)

        rec = se.BinDatRecordingExtractor(raw_filename, info['sample_rate'], info['num_chan'],
                                                                        info['dtype'], frames_first=info['frames_first'])
        se.load_probe_file(rec, prb_filename)
        
        recording_dict[rec_name] = rec
    
    return recording_dict

def get_ground_truths(study_folder):
    study_folder = Path(study_folder)
    rec_names = get_rec_names(study_folder)
    ground_truths = {}
    for rec_name in rec_names:
        sorting = se.NpzSortingExtractor(study_folder / 'ground_truth' / (rec_name+'.npz'))
        ground_truths[rec_name] = sorting
    return ground_truths
    
    
    
def run_study_sorters(study_folder, sorter_list, sorter_params={}, mode='keep',
                                        engine='loop', engine_kargs={}):
    study_folder = Path(study_folder)
    sorter_outputs = study_folder / 'sorter_outputs'
    
    recording_dict = get_recordings(study_folder)
    
    run_sorters(sorter_list, recording_dict,  sorter_outputs, sorter_params=sorter_params,
                    grouping_property=None, mode=mode, engine=engine, engine_kargs=engine_kargs,
                    with_output=False)



def collect_run_times(study_folder):
    """
    Collect run times in a working folder

    The output is list of (rec_name, sorter_name, run_time)
    """
    study_folder = Path(study_folder)
    sorter_outputs = study_folder / 'sorter_outputs'
    
    run_times = []
    for rec_name, sorter_name, output_folder in loop_over_folders(sorter_outputs):
        if os.path.exists(output_folder / 'run_log.txt'):
            with open(output_folder / 'run_log.txt', mode='r') as logfile:
                run_time = float(logfile.readline().replace('run_time:', ''))
            run_times.append((rec_name, sorter_name, run_time))
    return run_times




def aggregate_sorting_comparison(study_folder, exhaustive_gt=False, **karg_thresh):
    """
    Loop over output folder in a tree to collect sorting output and run 
    ground_truth_comparison on them.
    
    Parameters
    ----------
    study_folder: str
        The folrder where sorter.run_sorters have done the job.
    exhaustive_gt: bool (default True)
        Tell if the ground true is "exhaustive" or not. In other world if the
        GT have all possible units. It allows more performance measurment.
        For instance, MEArec simulated dataset have exhaustive_gt=True
    **karg_thresh: 
        Extra thresh kkargs are passed to 
        GroundTruthComparison.get_well_detected_units for
        See doc there.

    Returns
    ----------
    comparisons: a dict of SortingComparison

    out_dataframes: a dict of DataFrame
        Return several usefull DataFrame to compare all results:
          * run_times
          * performances
    """

    study_folder = Path(study_folder)
    sorter_outputs = study_folder / 'sorter_outputs'
    
    ground_truths = get_ground_truths(study_folder)
    results = collect_sorting_outputs(sorter_outputs)
    
    comparisons = {}
    for (rec_name,sorter_name), sorting in results.items():
        gt_sorting = ground_truths[rec_name]
        sc = compare_sorter_to_ground_truth(gt_sorting, sorting)
        comparisons[(rec_name, sorter_name)] = sc

    return comparisons



def aggregate_performances_table(study_folder,  exhaustive_gt=False, **karg_thresh):
    study_folder = Path(study_folder)
    sorter_outputs = study_folder / 'sorter_outputs'
    
    
    comparisons = aggregate_sorting_comparison(study_folder, exhaustive_gt=exhaustive_gt, **karg_thresh)
    ground_truths = get_ground_truths(study_folder)
    results = collect_sorting_outputs(sorter_outputs)
    
    study_folder = Path(study_folder)

    out_dataframes = {}


    # get run times:
    rt = collect_run_times(study_folder)
    run_times = pd.DataFrame(rt, columns=['rec_name', 'sorter_name', 'run_time'])
    run_times = run_times.set_index(['rec_name', 'sorter_name',])
    out_dataframes['run_times'] = run_times

    perf_pooled_with_sum = pd.DataFrame(index=run_times.index, columns=_perf_keys)
    out_dataframes['perf_pooled_with_sum'] = perf_pooled_with_sum

    perf_pooled_with_average = pd.DataFrame(index=run_times.index, columns=_perf_keys)
    out_dataframes['perf_pooled_with_average'] = perf_pooled_with_average
    
    count_units = pd.DataFrame(index=run_times.index, columns=['num_gt', 'num_sorter', 'num_well_detected', 'num_redundant'])
    out_dataframes['count_units'] = count_units
    if exhaustive_gt:
        count_units['num_false_positive'] = None
        count_units['num_bad'] = None
    
    
    for (rec_name, sorter_name), comp in comparisons.items():
        gt_sorting = ground_truths[rec_name]
        sorting = results[(rec_name, sorter_name)]
        
        perf = comp.get_performance(method='pooled_with_sum', output='pandas')
        perf_pooled_with_sum.loc[(rec_name, sorter_name), :] = perf

        perf = comp.get_performance(method='pooled_with_average', output='pandas')
        perf_pooled_with_average.loc[(rec_name, sorter_name), :] = perf
        
        count_units.loc[(rec_name, sorter_name), 'num_gt'] = len(gt_sorting.get_unit_ids())
        count_units.loc[(rec_name, sorter_name), 'num_sorter'] = len(sorting.get_unit_ids())
        count_units.loc[(rec_name, sorter_name), 'num_well_detected'] = comp.count_well_detected_units(**karg_thresh)
        count_units.loc[(rec_name, sorter_name), 'num_redundant'] = comp.count_redundant_units()
        if exhaustive_gt:
            count_units.loc[(rec_name, sorter_name), 'num_false_positive'] = comp.count_false_positive_units()
            count_units.loc[(rec_name, sorter_name), 'num_bad'] = comp.count_bad_units()

    return out_dataframes    
    
    
    
    
    
    