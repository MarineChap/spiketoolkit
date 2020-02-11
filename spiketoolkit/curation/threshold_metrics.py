from spiketoolkit.validation import MetricData
from spiketoolkit.validation import AmplitudeCutoff
from spiketoolkit.validation import SilhouetteScore
from spiketoolkit.validation import NumSpikes
from spiketoolkit.validation import DPrime
from spiketoolkit.validation import LRatio
from spiketoolkit.validation import FiringRate
from spiketoolkit.validation import PresenceRatio
from spiketoolkit.validation import ISIViolation
from spiketoolkit.validation import SNR
from spiketoolkit.validation import IsolationDistance
from spiketoolkit.validation import get_recording_params, get_amplitude_params, get_pca_scores_params, get_metric_scope_params, update_param_dicts

def threshold_num_spikes(
    sorting,
    threshold,
    threshold_sign,
    epoch=0,
    sampling_frequency=None,
    metric_scope_params=get_metric_scope_params(),
    save_as_property=True
):
    """
    Computes and thresholds the num spikes in the sorted dataset with the given sign and value.

    Parameters
    ----------
    sorting: SortingExtractor
        The sorting result to be evaluated.
    threshold: int or float
        The threshold for the given metric.
    threshold_sign: str
        If 'less', will threshold any metric less than the given threshold.
        If 'less_or_equal', will threshold any metric less than or equal to the given threshold.
        If 'greater', will threshold any metric greater than the given threshold.
        If 'greater_or_equal', will threshold any metric greater than or equal to the given threshold.
    epoch: int
        The threshold will be applied to the specified epoch.
        If epoch is None, then it will default to the first epoch.
    sampling_frequency:
        The sampling frequency of the result. If None, will check to see if sampling frequency is in sorting extractor.
    metric_scope_param: dict
        This dictionary should contain any subset of the following parameters:
            unit_ids: list
                List of unit ids to compute metric for. If not specified, all units are used
            epoch_tuples: list
                A list of tuples with a start and end time for each epoch
            epoch_names: list
                A list of strings for the names of the given epochs.
    save_features_props: bool
        If true, it will save amplitudes in the sorting extractor.
    save_as_property: bool
        If True, the metric is saved as sorting property
    Returns
    ----------
    threshold sorting extractor
    """
    if sampling_frequency is None and sorting.get_sampling_frequency() is None:
        raise ValueError(
            "Please pass in a sampling frequency (your SortingExtractor does not have one specified)"
        )
    elif sampling_frequency is None:
        sampling_frequency = sorting.get_sampling_frequency()

    ms_dict, = update_param_dicts(metric_scope_params=metric_scope_params)

    if ms_dict["unit_ids"] is None:
        ms_dict["unit_ids"] = sorting.get_unit_ids()

    md = MetricData(
        sorting=sorting,
        unit_ids=ms_dict["unit_ids"],
        epoch_tuples=ms_dict["epoch_tuples"],
        epoch_names=ms_dict["epoch_names"],
    )

    ns = NumSpikes(metric_data=md)
    threshold_sorting = ns.threshold_metric(threshold, threshold_sign, epoch, save_as_property)
    return threshold_sorting

def threshold_firing_rates(
    sorting,
    threshold,
    threshold_sign,
    epoch=0,
    sampling_frequency=None,
    metric_scope_params=get_metric_scope_params(),
    save_as_property=True
):
    """
    Computes and thresholds the firing rates in the sorted dataset with the given sign and value.

    Parameters
    ----------
    sorting: SortingExtractor
        The sorting result to be evaluated.
    threshold: int or float
        The threshold for the given metric.
    threshold_sign: str
        If 'less', will threshold any metric less than the given threshold.
        If 'less_or_equal', will threshold any metric less than or equal to the given threshold.
        If 'greater', will threshold any metric greater than the given threshold.
        If 'greater_or_equal', will threshold any metric greater than or equal to the given threshold.
    epoch: int
        The threshold will be applied to the specified epoch.
        If epoch is None, then it will default to the first epoch.
    sampling_frequency:
        The sampling frequency of the result. If None, will check to see if sampling frequency is in sorting extractor.
    metric_scope_param: dict
        This dictionary should contain any subset of the following parameters:
            unit_ids: list
                List of unit ids to compute metric for. If not specified, all units are used
            epoch_tuples: list
                A list of tuples with a start and end time for each epoch
            epoch_names: list
                A list of strings for the names of the given epochs.
    save_features_props: bool
        If true, it will save amplitudes in the sorting extractor.
    save_as_property: bool
        If True, the metric is saved as sorting property
    Returns
    ----------
    threshold sorting extractor
    """
    if sampling_frequency is None and sorting.get_sampling_frequency() is None:
        raise ValueError(
            "Please pass in a sampling frequency (your SortingExtractor does not have one specified)"
        )
    elif sampling_frequency is None:
        sampling_frequency = sorting.get_sampling_frequency()

    ms_dict, = update_param_dicts(metric_scope_params=metric_scope_params)

    if ms_dict["unit_ids"] is None:
        ms_dict["unit_ids"] = sorting.get_unit_ids()

    md = MetricData(
        sorting=sorting,
        unit_ids=ms_dict["unit_ids"],
        epoch_tuples=ms_dict["epoch_tuples"],
        epoch_names=ms_dict["epoch_names"],
    )

    fr = FiringRate(metric_data=md)
    threshold_sorting = fr.threshold_metric(threshold, threshold_sign, epoch, save_as_property)
    return threshold_sorting


def threshold_presence_ratios(
    sorting,
    threshold,
    threshold_sign,
    epoch=0,
    sampling_frequency=None,
    metric_scope_params=get_metric_scope_params(),
    save_as_property=True
):
    """
    Computes and thresholds the presence ratios in the sorted dataset with the given sign and value.

    Parameters
    ----------
    sorting: SortingExtractor
        The sorting result to be evaluated.
    threshold: int or float
        The threshold for the given metric.
    threshold_sign: str
        If 'less', will threshold any metric less than the given threshold.
        If 'less_or_equal', will threshold any metric less than or equal to the given threshold.
        If 'greater', will threshold any metric greater than the given threshold.
        If 'greater_or_equal', will threshold any metric greater than or equal to the given threshold.
    epoch:
        The threshold will be applied to the specified epoch.
        If epoch is None, then it will default to the first epoch.
    sampling_frequency:
        The sampling frequency of the result. If None, will check to see if sampling frequency is in sorting extractor.
    metric_scope_param: dict
        This dictionary should contain any subset of the following parameters:
            unit_ids: list
                List of unit ids to compute metric for. If not specified, all units are used
            epoch_tuples: list
                A list of tuples with a start and end time for each epoch
            epoch_names: list
                A list of strings for the names of the given epochs.
    save_features_props: bool
        If true, it will save amplitudes in the sorting extractor.
    save_as_property: bool
        If True, the metric is saved as sorting property
    Returns
    ----------
    threshold sorting extractor
    """
    if sampling_frequency is None and sorting.get_sampling_frequency() is None:
        raise ValueError(
            "Please pass in a sampling frequency (your SortingExtractor does not have one specified)"
        )
    elif sampling_frequency is None:
        sampling_frequency = sorting.get_sampling_frequency()

    ms_dict, = update_param_dicts(metric_scope_params=metric_scope_params)

    if ms_dict["unit_ids"] is None:
        ms_dict["unit_ids"] = sorting.get_unit_ids()

    md = MetricData(
        sorting=sorting,
        unit_ids=ms_dict["unit_ids"],
        epoch_tuples=ms_dict["epoch_tuples"],
        epoch_names=ms_dict["epoch_names"],
    )

    pr = PresenceRatio(metric_data=md)
    threshold_sorting = pr.threshold_metric(threshold, threshold_sign, epoch, save_as_property)
    return threshold_sorting

def threshold_isi_violations(
    sorting,
    threshold,
    threshold_sign,
    epoch=0,
    isi_threshold=0.0015, 
    min_isi=0.000166,
    sampling_frequency=None,
    metric_scope_params=get_metric_scope_params(),
    save_as_property=True
):
    """
    Computes and thresholds the isi violations in the sorted dataset with the given sign and value.

    Parameters
    ----------
    sorting: SortingExtractor
        The sorting result to be evaluated.
    threshold: int or float
        The threshold for the given metric.
    threshold_sign: str
        If 'less', will threshold any metric less than the given threshold.
        If 'less_or_equal', will threshold any metric less than or equal to the given threshold.
        If 'greater', will threshold any metric greater than the given threshold.
        If 'greater_or_equal', will threshold any metric greater than or equal to the given threshold.
    epoch: int
        The threshold will be applied to the specified epoch.
        If epoch is None, then it will default to the first epoch.
    isi_threshold: float
        The isi threshold for calculating isi violations.
    min_isi: float
        The minimum expected isi value.
    sampling_frequency:
        The sampling frequency of the result. If None, will check to see if sampling frequency is in sorting extractor.
    metric_scope_param: dict
        This dictionary should contain any subset of the following parameters:
            unit_ids: list
                List of unit ids to compute metric for. If not specified, all units are used
            epoch_tuples: list
                A list of tuples with a start and end time for each epoch
            epoch_names: list
                A list of strings for the names of the given epochs.
    save_features_props: bool
        If true, it will save amplitudes in the sorting extractor.
    save_as_property: bool
        If True, the metric is saved as sorting property
    Returns
    ----------
    threshold sorting extractor
    """
    if sampling_frequency is None and sorting.get_sampling_frequency() is None:
        raise ValueError(
            "Please pass in a sampling frequency (your SortingExtractor does not have one specified)"
        )
    elif sampling_frequency is None:
        sampling_frequency = sorting.get_sampling_frequency()

    ms_dict, = update_param_dicts(metric_scope_params=metric_scope_params)

    if ms_dict["unit_ids"] is None:
        ms_dict["unit_ids"] = sorting.get_unit_ids()

    md = MetricData(
        sorting=sorting,
        unit_ids=ms_dict["unit_ids"],
        epoch_tuples=ms_dict["epoch_tuples"],
        epoch_names=ms_dict["epoch_names"],
    )

    iv = ISIViolation(metric_data=md)
    threshold_sorting = iv.threshold_metric(threshold, threshold_sign, epoch, isi_threshold, min_isi, save_as_property)
    return threshold_sorting

def threshold_amplitude_cutoffs(
    sorting,
    recording,
    threshold,
    threshold_sign,
    epoch=0,
    recording_params=get_recording_params(),
    amplitude_params=get_amplitude_params(),
    metric_scope_params=get_metric_scope_params(),
    save_features_props=False,
    seed=None,
    save_as_property=True
):
    """
    Computes and thresholds the amplitude cutoffs in the sorted dataset with the given sign and value.

    Parameters
    ----------
    sorting: SortingExtractor
        The sorting result to be evaluated.
    recording: RecordingExtractor
        The given recording extractor from which to extract amplitudes
    threshold: int or float
        The threshold for the given metric.
    threshold_sign: str
        If 'less', will threshold any metric less than the given threshold.
        If 'less_or_equal', will threshold any metric less than or equal to the given threshold.
        If 'greater', will threshold any metric greater than the given threshold.
        If 'greater_or_equal', will threshold any metric greater than or equal to the given threshold.
    epoch: int
        The threshold will be applied to the specified epoch.
        If epoch is None, then it will default to the first epoch.
    amplitude_params: dict
        This dictionary should contain any subset of the following parameters:
            amp_method: str
                If 'absolute' (default), amplitudes are absolute amplitudes in uV are returned.
                If 'relative', amplitudes are returned as ratios between waveform amplitudes and template amplitudes.
            amp_peak: str
                If maximum channel has to be found among negative peaks ('neg'), positive ('pos') or both ('both' - default)
            amp_frames_before: int
                Frames before peak to compute amplitude.
            amp_frames_after: int
                Frames after peak to compute amplitude.
    recording_params: dict
        This dictionary should contain any subset of the following parameters:
            apply_filter: bool
                If True, recording is bandpass-filtered.
            freq_min: float
                High-pass frequency for optional filter (default 300 Hz).
            freq_max: float
                Low-pass frequency for optional filter (default 6000 Hz).
    quality_metric_params: dict
        This dictionary should contain any subset of the following parameters:
            unit_ids: list
                List of unit ids to compute metric for. If not specified, all units are used
            epoch_tuples: list
                A list of tuples with a start and end time for each epoch
            epoch_names: list
                A list of strings for the names of the given epochs.
    save_features_props: bool
        If true, it will save amplitudes in the sorting extractor.
    seed: int
        Random seed for reproducibility
    save_as_property: bool
        If True, the metric is saved as sorting property
    Returns
    ----------
    threshold sorting extractor
    """
    rp_dict, ap_dict, ms_dict = update_param_dicts(recording_params=recording_params, 
                                                   amplitude_params=amplitude_params, 
                                                   metric_scope_params=metric_scope_params)
    if ms_dict["unit_ids"] is None:
        ms_dict["unit_ids"] = sorting.get_unit_ids()

    md = MetricData(
        sorting=sorting,
        recording=recording,
        apply_filter=rp_dict["apply_filter"],
        freq_min=rp_dict["freq_min"],
        freq_max=rp_dict["freq_max"],
        unit_ids=ms_dict["unit_ids"],
        epoch_tuples=ms_dict["epoch_tuples"],
        epoch_names=ms_dict["epoch_names"],
    )
    md.compute_amplitudes(
        amp_method=ap_dict["amp_method"],
        amp_peak=ap_dict["amp_peak"],
        amp_frames_before=ap_dict["amp_frames_before"],
        amp_frames_after=ap_dict["amp_frames_after"],
        save_features_props=save_features_props,
        seed=seed,
    )
    ac = AmplitudeCutoff(metric_data=md)
    threshold_sorting = ac.threshold_metric(threshold, threshold_sign, epoch, save_as_property)
    return threshold_sorting

def threshold_snrs(
    sorting,
    recording,
    threshold,
    threshold_sign,
    epoch=0,
    snr_mode="mad",
    snr_noise_duration=10.0,
    max_spikes_per_unit_for_snr=1000,
    template_mode="median", 
    max_channel_peak="both", 
    recording_params=get_recording_params(),
    metric_scope_params=get_metric_scope_params(),
    recompute_info=True,
    save_features_props=True,
    save_as_property=True,
    seed=None,
):
    """
    Computes and thresholds the snrs in the sorted dataset with the given sign and value.

    Parameters
    ----------
    sorting: SortingExtractor
        The sorting result to be evaluated.

    recording: RecordingExtractor
        The given recording extractor from which to extract amplitudes

    threshold: int or float
        The threshold for the given metric.

    threshold_sign: str
        If 'less', will threshold any metric less than the given threshold.
        If 'less_or_equal', will threshold any metric less than or equal to the given threshold.
        If 'greater', will threshold any metric greater than the given threshold.
        If 'greater_or_equal', will threshold any metric greater than or equal to the given threshold.

    epoch: int
        The threshold will be applied to the specified epoch.
        If epoch is None, then it will default to the first epoch.

    snr_mode: str
            Mode to compute noise SNR ('mad' | 'std' - default 'mad')
            
    snr_noise_duration: float
        Number of seconds to compute noise level from (default 10.0)

    max_spikes_per_unit_for_snr: int
        Maximum number of spikes to compute templates from (default 1000)

    template_mode: str
        Use 'mean' or 'median' to compute templates

    max_channel_peak: str
        If maximum channel has to be found among negative peaks ('neg'), positive ('pos') or both ('both' - default)

    pca_scores_params: dict
        This dictionary should contain any subset of the following parameters:
            ms_before: float
                Time period in ms to cut waveforms before the spike events
            ms_after: float
                Time period in ms to cut waveforms after the spike events
            dtype: dtype
                The numpy dtype of the waveforms
            max_spikes_per_unit: int
                The maximum number of spikes to extract per unit.
            max_spikes_for_pca: int
                The maximum number of spikes to use to compute PCA.

    recording_params: dict
        This dictionary should contain any subset of the following parameters:
            apply_filter: bool
                If True, recording is bandpass-filtered.
            freq_min: float
                High-pass frequency for optional filter (default 300 Hz).
            freq_max: float
                Low-pass frequency for optional filter (default 6000 Hz).

    metric_scope_params: dict
        This dictionary should contain any subset of the following parameters:
            unit_ids: list
                unit ids to compute metric for. If not specified, all units are used
            epoch_tuples: list
                A list of tuples with a start and end time for each epoch
            epoch_names: list
                A list of strings for the names of the given epochs.

    recompute_info: bool
            If True, waveforms are recomputed

    save_features_props: bool
        If true, it will save amplitudes in the sorting extractor.

    save_as_property: bool
        If True, the metric is saved as sorting property

    seed: int
        Random seed for reproducibility

    Returns
    ----------
    threshold sorting extractor
    """
    rp_dict, ms_dict = update_param_dicts(recording_params=recording_params, 
                                          metric_scope_params=metric_scope_params)

    if ms_dict["unit_ids"] is None:
        ms_dict["unit_ids"] = sorting.get_unit_ids()

    md = MetricData(
        sorting=sorting,
        recording=recording,
        apply_filter=rp_dict["apply_filter"],
        freq_min=rp_dict["freq_min"],
        freq_max=rp_dict["freq_max"],
        unit_ids=ms_dict["unit_ids"],
        epoch_tuples=ms_dict["epoch_tuples"],
        epoch_names=ms_dict["epoch_names"],
    )

    snr = SNR(metric_data=md)
    threshold_sorting = snr.threshold_metric(threshold, threshold_sign, epoch, snr_mode, snr_noise_duration, 
                                             max_spikes_per_unit_for_snr, template_mode, max_channel_peak, 
                                             save_features_props, recompute_info, seed, save_as_property)
    return threshold_sorting

def threshold_silhouette_scores(
    sorting,
    recording,
    threshold,
    threshold_sign,
    epoch=0,
    max_spikes_for_silhouette = 10000,
    recording_params=get_recording_params(),
    pca_scores_params=get_pca_scores_params(),
    metric_scope_params=get_metric_scope_params(),
    save_features_props=False,
    seed=None,
    save_as_property=True
):
    """
    Computes and thresholds the silhouette scores in the sorted dataset with the given sign and value.

    Parameters
    ----------
    sorting: SortingExtractor
        The sorting result to be evaluated.

    recording: RecordingExtractor
        The given recording extractor from which to extract amplitudes

    threshold: int or float
        The threshold for the given metric.

    threshold_sign: str
        If 'less', will threshold any metric less than the given threshold.
        If 'less_or_equal', will threshold any metric less than or equal to the given threshold.
        If 'greater', will threshold any metric greater than the given threshold.
        If 'greater_or_equal', will threshold any metric greater than or equal to the given threshold.

    epoch: int
        The threshold will be applied to the specified epoch.
        If epoch is None, then it will default to the first epoch.

    max_spikes_for_silhouette: int
        Max spikes to be used for silhouette metric.

    recording_params: dict
        This dictionary should contain any subset of the following parameters:
            apply_filter: bool
                If True, recording is bandpass-filtered.
            freq_min: float
                High-pass frequency for optional filter (default 300 Hz).
            freq_max: float
                Low-pass frequency for optional filter (default 6000 Hz).

    pca_scores_params: dict
        This dictionary should contain any subset of the following parameters:
            ms_before: float
                Time period in ms to cut waveforms before the spike events
            ms_after: float
                Time period in ms to cut waveforms after the spike events
            dtype: dtype
                The numpy dtype of the waveforms
            max_spikes_per_unit: int
                The maximum number of spikes to extract per unit.
            max_spikes_for_pca: int
                The maximum number of spikes to use to compute PCA.

    metric_scope_params: dict
        This dictionary should contain any subset of the following parameters:
            unit_ids: list
                unit ids to compute metric for. If not specified, all units are used
            epoch_tuples: list
                A list of tuples with a start and end time for each epoch
            epoch_names: list
                A list of strings for the names of the given epochs.

    save_features_props: bool
        If true, it will save amplitudes in the sorting extractor.

    save_as_property: bool
        If True, the metric is saved as sorting property

    seed: int
        Random seed for reproducibility
    
    save_as_property: bool
        If True, the metric is saved as sorting property

    Returns
    ----------
    threshold sorting extractor
    """
    rp_dict, ps_dict, ms_dict = update_param_dicts(recording_params=recording_params, 
                                                   pca_scores_params=pca_scores_params, 
                                                   metric_scope_params=metric_scope_params)

    if ms_dict["unit_ids"] is None:
        ms_dict["unit_ids"] = sorting.get_unit_ids()

    metric_data = MetricData(
        sorting=sorting,
        recording=recording,
        apply_filter=rp_dict["apply_filter"],
        freq_min=rp_dict["freq_min"],
        freq_max=rp_dict["freq_max"],
        unit_ids=ms_dict["unit_ids"],
        epoch_tuples=ms_dict["epoch_tuples"],
        epoch_names=ms_dict["epoch_names"],
    )

    metric_data.compute_pca_scores(
        n_comp=ps_dict["n_comp"],
        ms_before=ps_dict["ms_before"],
        ms_after=ps_dict["ms_after"],
        dtype=ps_dict["dtype"],
        max_spikes_per_unit=ps_dict["max_spikes_per_unit"],
        max_spikes_for_pca=ps_dict["max_spikes_for_pca"],
        save_features_props=save_features_props,
        seed=seed,
    )

    silhouette_score = SilhouetteScore(metric_data=metric_data)
    threshold_sorting = silhouette_score.threshold_metric(
        threshold, threshold_sign, epoch, max_spikes_for_silhouette, seed, save_as_property)
    return threshold_sorting


def threshold_d_primes(
    sorting,
    recording,
    threshold,
    threshold_sign,
    epoch=0,
    num_channels_to_compare=13,
    max_spikes_per_cluster=500,
    recording_params=get_recording_params(),
    pca_scores_params=get_pca_scores_params(),
    metric_scope_params=get_metric_scope_params(),
    save_features_props=False,
    seed=None,
    save_as_property=True
):
    """
    Computes and thresholds the d primes in the sorted dataset with the given sign and value.

    Parameters
    ----------
    sorting: SortingExtractor
        The sorting result to be evaluated.

    recording: RecordingExtractor
        The given recording extractor from which to extract amplitudes

    threshold: int or float
        The threshold for the given metric.

    threshold_sign: str
        If 'less', will threshold any metric less than the given threshold.
        If 'less_or_equal', will threshold any metric less than or equal to the given threshold.
        If 'greater', will threshold any metric greater than the given threshold.
        If 'greater_or_equal', will threshold any metric greater than or equal to the given threshold.

    epoch: int
        The threshold will be applied to the specified epoch.
        If epoch is None, then it will default to the first epoch.

    num_channels_to_compare: int
        The number of channels to be used for the PC extraction and comparison
        
    max_spikes_per_cluster: int
        Max spikes to be used from each unit

    recording_params: dict
        This dictionary should contain any subset of the following parameters:
            apply_filter: bool
                If True, recording is bandpass-filtered.
            freq_min: float
                High-pass frequency for optional filter (default 300 Hz).
            freq_max: float
                Low-pass frequency for optional filter (default 6000 Hz).

    pca_scores_params: dict
        This dictionary should contain any subset of the following parameters:
            ms_before: float
                Time period in ms to cut waveforms before the spike events
            ms_after: float
                Time period in ms to cut waveforms after the spike events
            dtype: dtype
                The numpy dtype of the waveforms
            max_spikes_per_unit: int
                The maximum number of spikes to extract per unit.
            max_spikes_for_pca: int
                The maximum number of spikes to use to compute PCA.

    metric_scope_params: dict
        This dictionary should contain any subset of the following parameters:
            unit_ids: list
                unit ids to compute metric for. If not specified, all units are used
            epoch_tuples: list
                A list of tuples with a start and end time for each epoch
            epoch_names: list
                A list of strings for the names of the given epochs.

    save_features_props: bool
        If true, it will save amplitudes in the sorting extractor.

    save_as_property: bool
        If True, the metric is saved as sorting property

    seed: int
        Random seed for reproducibility
    
    save_as_property: bool
        If True, the metric is saved as sorting property

    Returns
    ----------
    threshold sorting extractor
    """
    rp_dict, ps_dict, ms_dict = update_param_dicts(recording_params=recording_params, 
                                                   pca_scores_params=pca_scores_params, 
                                                   metric_scope_params=metric_scope_params)

    if ms_dict["unit_ids"] is None:
        ms_dict["unit_ids"] = sorting.get_unit_ids()

    md = MetricData(
        sorting=sorting,
        recording=recording,
        apply_filter=rp_dict["apply_filter"],
        freq_min=rp_dict["freq_min"],
        freq_max=rp_dict["freq_max"],
        unit_ids=ms_dict["unit_ids"],
        epoch_tuples=ms_dict["epoch_tuples"],
        epoch_names=ms_dict["epoch_names"],
    )

    md.compute_pca_scores(
        n_comp=ps_dict["n_comp"],
        ms_before=ps_dict["ms_before"],
        ms_after=ps_dict["ms_after"],
        dtype=ps_dict["dtype"],
        max_spikes_per_unit=ps_dict["max_spikes_per_unit"],
        max_spikes_for_pca=ps_dict["max_spikes_for_pca"],
        save_features_props=save_features_props,
        seed=seed,
    )

    d_prime = DPrime(metric_data=md)
    threshold_sorting = d_prime.threshold_metric(threshold, threshold_sign, epoch, num_channels_to_compare, 
                                                 max_spikes_per_cluster, seed, save_as_property)
    return threshold_sorting


def threshold_l_ratios(
    sorting,
    recording,
    threshold,
    threshold_sign,
    epoch=0,
    num_channels_to_compare=13,
    max_spikes_per_cluster=500,
    recording_params=get_recording_params(),
    pca_scores_params=get_pca_scores_params(),
    metric_scope_params=get_metric_scope_params(),
    save_features_props=False,
    seed=None,
    save_as_property=True
):
    """
    Computes and thresholds the l ratios in the sorted dataset with the given sign and value.

    Parameters
    ----------
    sorting: SortingExtractor
        The sorting result to be evaluated.

    recording: RecordingExtractor
        The given recording extractor from which to extract amplitudes

    threshold: int or float
        The threshold for the given metric.

    threshold_sign: str
        If 'less', will threshold any metric less than the given threshold.
        If 'less_or_equal', will threshold any metric less than or equal to the given threshold.
        If 'greater', will threshold any metric greater than the given threshold.
        If 'greater_or_equal', will threshold any metric greater than or equal to the given threshold.

    epoch: int
        The threshold will be applied to the specified epoch.
        If epoch is None, then it will default to the first epoch.

    num_channels_to_compare: int
        The number of channels to be used for the PC extraction and comparison
        
    max_spikes_per_cluster: int
        Max spikes to be used from each unit

    recording_params: dict
        This dictionary should contain any subset of the following parameters:
            apply_filter: bool
                If True, recording is bandpass-filtered.
            freq_min: float
                High-pass frequency for optional filter (default 300 Hz).
            freq_max: float
                Low-pass frequency for optional filter (default 6000 Hz).

    pca_scores_params: dict
        This dictionary should contain any subset of the following parameters:
            ms_before: float
                Time period in ms to cut waveforms before the spike events
            ms_after: float
                Time period in ms to cut waveforms after the spike events
            dtype: dtype
                The numpy dtype of the waveforms
            max_spikes_per_unit: int
                The maximum number of spikes to extract per unit.
            max_spikes_for_pca: int
                The maximum number of spikes to use to compute PCA.

    metric_scope_params: dict
        This dictionary should contain any subset of the following parameters:
            unit_ids: list
                unit ids to compute metric for. If not specified, all units are used
            epoch_tuples: list
                A list of tuples with a start and end time for each epoch
            epoch_names: list
                A list of strings for the names of the given epochs.

    save_features_props: bool
        If true, it will save amplitudes in the sorting extractor.

    save_as_property: bool
        If True, the metric is saved as sorting property

    seed: int
        Random seed for reproducibility
    
    save_as_property: bool
        If True, the metric is saved as sorting property

    Returns
    ----------
    threshold sorting extractor
    """
    rp_dict, ps_dict, ms_dict = update_param_dicts(recording_params=recording_params, 
                                                   pca_scores_params=pca_scores_params, 
                                                   metric_scope_params=metric_scope_params)

    if ms_dict["unit_ids"] is None:
        ms_dict["unit_ids"] = sorting.get_unit_ids()

    md = MetricData(
        sorting=sorting,
        recording=recording,
        apply_filter=rp_dict["apply_filter"],
        freq_min=rp_dict["freq_min"],
        freq_max=rp_dict["freq_max"],
        unit_ids=ms_dict["unit_ids"],
        epoch_tuples=ms_dict["epoch_tuples"],
        epoch_names=ms_dict["epoch_names"],
    )

    md.compute_pca_scores(
        n_comp=ps_dict["n_comp"],
        ms_before=ps_dict["ms_before"],
        ms_after=ps_dict["ms_after"],
        dtype=ps_dict["dtype"],
        max_spikes_per_unit=ps_dict["max_spikes_per_unit"],
        max_spikes_for_pca=ps_dict["max_spikes_for_pca"],
        save_features_props=save_features_props,
        seed=seed,
    )

    l_ratio = LRatio(metric_data=md)
    threshold_sorting = l_ratio.threshold_metric(threshold, threshold_sign, epoch, num_channels_to_compare, 
                                                 max_spikes_per_cluster, seed, save_as_property)
    return threshold_sorting

def threshold_isolation_distances(
    sorting,
    recording,
    threshold,
    threshold_sign,
    epoch=0,
    num_channels_to_compare=13,
    max_spikes_per_cluster=500,
    recording_params=get_recording_params(),
    pca_scores_params=get_pca_scores_params(),
    metric_scope_params=get_metric_scope_params(),
    save_features_props=False,
    seed=None,
    save_as_property=True
):
    """
    Computes and thresholds the isolation distances in the sorted dataset with the given sign and value.

    Parameters
    ----------
    sorting: SortingExtractor
        The sorting result to be evaluated.

    recording: RecordingExtractor
        The given recording extractor from which to extract amplitudes

    threshold: int or float
        The threshold for the given metric.

    threshold_sign: str
        If 'less', will threshold any metric less than the given threshold.
        If 'less_or_equal', will threshold any metric less than or equal to the given threshold.
        If 'greater', will threshold any metric greater than the given threshold.
        If 'greater_or_equal', will threshold any metric greater than or equal to the given threshold.

    epoch: int
        The threshold will be applied to the specified epoch.
        If epoch is None, then it will default to the first epoch.

    num_channels_to_compare: int
        The number of channels to be used for the PC extraction and comparison
        
    max_spikes_per_cluster: int
        Max spikes to be used from each unit

    recording_params: dict
        This dictionary should contain any subset of the following parameters:
            apply_filter: bool
                If True, recording is bandpass-filtered.
            freq_min: float
                High-pass frequency for optional filter (default 300 Hz).
            freq_max: float
                Low-pass frequency for optional filter (default 6000 Hz).

    pca_scores_params: dict
        This dictionary should contain any subset of the following parameters:
            ms_before: float
                Time period in ms to cut waveforms before the spike events
            ms_after: float
                Time period in ms to cut waveforms after the spike events
            dtype: dtype
                The numpy dtype of the waveforms
            max_spikes_per_unit: int
                The maximum number of spikes to extract per unit.
            max_spikes_for_pca: int
                The maximum number of spikes to use to compute PCA.

    metric_scope_params: dict
        This dictionary should contain any subset of the following parameters:
            unit_ids: list
                unit ids to compute metric for. If not specified, all units are used
            epoch_tuples: list
                A list of tuples with a start and end time for each epoch
            epoch_names: list
                A list of strings for the names of the given epochs.

    save_features_props: bool
        If true, it will save amplitudes in the sorting extractor.

    save_as_property: bool
        If True, the metric is saved as sorting property

    seed: int
        Random seed for reproducibility
    
    save_as_property: bool
        If True, the metric is saved as sorting property

    Returns
    ----------
    threshold sorting extractor
    """
    rp_dict, ps_dict, ms_dict = update_param_dicts(recording_params=recording_params, 
                                                   pca_scores_params=pca_scores_params, 
                                                   metric_scope_params=metric_scope_params)

    if ms_dict["unit_ids"] is None:
        ms_dict["unit_ids"] = sorting.get_unit_ids()

    md = MetricData(
        sorting=sorting,
        recording=recording,
        apply_filter=rp_dict["apply_filter"],
        freq_min=rp_dict["freq_min"],
        freq_max=rp_dict["freq_max"],
        unit_ids=ms_dict["unit_ids"],
        epoch_tuples=ms_dict["epoch_tuples"],
        epoch_names=ms_dict["epoch_names"],
    )

    md.compute_pca_scores(
        n_comp=ps_dict["n_comp"],
        ms_before=ps_dict["ms_before"],
        ms_after=ps_dict["ms_after"],
        dtype=ps_dict["dtype"],
        max_spikes_per_unit=ps_dict["max_spikes_per_unit"],
        max_spikes_for_pca=ps_dict["max_spikes_for_pca"],
        save_features_props=save_features_props,
        seed=seed,
    )

    isolaiton_distance = IsolationDistance(metric_data=md)
    threshold_sorting = isolaiton_distance.threshold_metric(threshold, threshold_sign, epoch, num_channels_to_compare, 
                                                            max_spikes_per_cluster, seed, save_as_property)
    return threshold_sorting