"""
I need help here because:
  * there is no spikeextractor in spikeextractor module
  * there is no output_folder

Reading the code do not make evident if there is a persistency on disk.

"""
import spiketoolkit as st
from ..tools import _spikeSortByProperty
import time

from spiketoolkit.sorters.basesorter import BaseSorter
import spikeextractors as se

try:
    import ml_ms4alg
    HAVE_MS4 = True
except ModuleNotFoundError:
    HAVE_MS4 = False


class Mountainsort4Sorter(BaseSorter):
    """
    Mountainsort
    """
    
    sorter_name = 'mountainsort4'
    installed = HAVE_MS4
    
    SortingExtractor_Class = None # there is not extractor !!!!!!!!!!!!!!!!!!!!!!!!
    
    _default_params = {
        'detect_sign': -1,  # Use -1, 0, or 1, depending on the sign of the spikes in the recording
        'adjacency_radius': -1,  # Use -1 to include all channels in every neighborhood
        'freq_min': 300,  # Use None for no bandpass filtering
        'freq_max': 6000,
        'whiten': True,  # Whether to do channel whitening as part of preprocessing
        'clip_size': 50,
        'detect_threshold': 3,
        'detect_interval': 10,  # Minimum number of timepoints between events detected on the same channel
        'noise_overlap_threshold': 0.15,  # Use None for no automated curation'
        'parallel': True
    }
    
    installation_mesg = """
       >>> pip install tridesclous
    
    More information on klusta at:
      * https://github.com/tridesclous/tridesclous
      * https://tridesclous.readthedocs.io
    """
    
    def __init__(self, **kargs):
        BaseSorter.__init__(self, **kargs)

    def _setup_recording(self, recording, output_folder):
        pass
        # Not done
    
    def _run(self, recording, output_folder):
        pass
        # Not done


#####################################
## OLD IMPLEMENTAtion ABOVE
#####################################

def mountainsort4(
        recording,  # The recording extractor
        output_folder=None,
        by_property=None,
        parallel=False,
        detect_sign=-1,  # Use -1, 0, or 1, depending on the sign of the spikes in the recording
        adjacency_radius=-1,  # Use -1 to include all channels in every neighborhood
        freq_min=300,  # Use None for no bandpass filtering
        freq_max=6000,
        whiten=True,  # Whether to do channel whitening as part of preprocessing
        clip_size=50,
        detect_threshold=3,
        detect_interval=10,  # Minimum number of timepoints between events detected on the same channel
        noise_overlap_threshold=0.15  # Use None for no automated curation
):
    t_start_proc = time.time()
    if by_property is None:
        sorting = _mountainsort4(recording, detect_sign, adjacency_radius, freq_min, freq_max,
                                 whiten, clip_size, detect_threshold, detect_interval, noise_overlap_threshold)
    else:
        if by_property in recording.getChannelPropertyNames():
            sorting = _spikeSortByProperty(recording, 'mountainsort', by_property, parallel, output_folder=output_folder,
                                           detect_sign=detect_sign, adjacency_radius=adjacency_radius,
                                           freq_min=freq_min, freq_max=freq_max, whiten=whiten, clip_size=clip_size,
                                           detect_threshold=detect_threshold, detect_interval=detect_interval,
                                           noise_overlap_threshold=noise_overlap_threshold)
        else:
            print("Property not available! Running normal spike sorting")
            sorting = _mountainsort4(recording, detect_sign, adjacency_radius, freq_min, freq_max,
                                     whiten, clip_size, detect_threshold, detect_interval, noise_overlap_threshold)

    print('Elapsed time: ', time.time() - t_start_proc)

    return sorting


def _mountainsort4(
        recording,  # The recording extractor
        detect_sign=-1,  # Use -1, 0, or 1, depending on the sign of the spikes in the recording
        adjacency_radius=-1,  # Use -1 to include all channels in every neighborhood
        freq_min=300,  # Use None for no bandpass filtering
        freq_max=6000,
        whiten=True,  # Whether to do channel whitening as part of preprocessing
        clip_size=50,
        detect_threshold=3,
        detect_interval=10,  # Minimum number of timepoints between events detected on the same channel
        noise_overlap_threshold=0.15  # Use None for no automated curation
):
    try:
        import ml_ms4alg
    except ModuleNotFoundError:
        raise ModuleNotFoundError("\nTo use Mountainsort, install ml_ms4alg: \n\n"
                                  "\npip install ml_ms4alg\n"
                                  "\nMore information on Mountainsort at: "
                                  "\nhttps://github.com/flatironinstitute/mountainsort")
    # Bandpass filter
    if freq_min is not None:
        recording = st.preprocessing.bandpass_filter(recording=recording, freq_min=freq_min, freq_max=freq_max)

    # Whiten
    if whiten:
        recording = st.preprocessing.whiten(recording=recording)

    # Check location
    if 'location' not in recording.getChannelPropertyNames():
        for i, chan in enumerate(recording.getChannelIds()):
            recording.setChannelProperty(chan, 'location', [0, i])

    # Sort
    sorting = ml_ms4alg.mountainsort4(
        recording=recording,
        detect_sign=detect_sign,
        adjacency_radius=adjacency_radius,
        clip_size=clip_size,
        detect_threshold=detect_threshold,
        detect_interval=detect_interval
    )

    # Curate
    if noise_overlap_threshold is not None:
        sorting = ml_ms4alg.mountainsort4_curation(
            recording=recording,
            sorting=sorting,
            noise_overlap_threshold=noise_overlap_threshold
        )

    return sorting


def mountainsort4_default_params():
    return {'detect_sign': -1,  # Use -1, 0, or 1, depending on the sign of the spikes in the recording
            'adjacency_radius': -1,  # Use -1 to include all channels in every neighborhood
            'freq_min': 300,  # Use None for no bandpass filtering
            'freq_max': 6000,
            'whiten': True,  # Whether to do channel whitening as part of preprocessing
            'clip_size': 50,
            'detect_threshold': 3,
            'detect_interval': 10,  # Minimum number of timepoints between events detected on the same channel
            'noise_overlap_threshold': 0.15,  # Use None for no automated curation'
            'parallel': True
            }
