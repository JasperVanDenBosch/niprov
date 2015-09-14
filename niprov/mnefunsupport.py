# -*- coding: utf-8 -*-
"""mnefun support module

This module provides handlers to attach to mnefun events.

::

    import mnefun
    import niprov.mnefunsupport
    params = mnefun.Params()
    params.on_process = niprov.mnefunsupport.handler

"""
import os
from niprov.dependencies import Dependencies
from niprov.discovery import discover
from niprov.logging import log


def handler(text, func, out, params, dependencies=Dependencies()):
    """mnefun on_process handler

    Responds to the following mnefun steps:
    fetch_raw_files: Runs discover on the subjects' raw data dirs.
    fetch_sss_files,
    apply_preprocessing_combined,
    save_epochs: For these steps, runs log for the new files.
    """
    listener = dependencies.getListener()
    libs = dependencies.getLibraries()

    funcname = func.func_name
    listener.mnefunEventReceived(funcname)
    paramdict = {}
    for param in provenanceParams:
        if hasattr(params, param):
            paramdict[param] = getattr(params, param)
    customprov = {'mnefun':paramdict}
    for subj in params.subjects:
        if funcname == 'fetch_raw_files':
            subjrawdir = os.path.join(params.work_dir, subj, params.raw_dir)
            discover(subjrawdir)
        elif funcname == 'fetch_sss_files':
            trans = 'Signal Space Separation'
            rawfiles = libs.mnefun.get_raw_fnames(params, subj, 'raw')
            sssfiles = libs.mnefun.get_raw_fnames(params, subj, 'sss')
            for rawfile, sssfile in zip(rawfiles, sssfiles):
                log(sssfile, trans, rawfile, provenance=customprov)
        elif funcname == 'apply_preprocessing_combined':
            trans = 'Signal Space Projection'
            sssfiles = libs.mnefun.get_raw_fnames(params, subj, 'sss')
            pcafiles = libs.mnefun.get_raw_fnames(params, subj, 'pca')
            for sssfile, pcafile in zip(sssfiles, pcafiles):
                log(pcafile, trans, sssfile, provenance=customprov)
        elif funcname == 'save_epochs':
            pcafiles = libs.mnefun.get_raw_fnames(params, subj, 'pca')
            evtfiles = libs.mnefun._paths.get_epochs_evokeds_fnames(params, 
                subj, params.analyses)
            for evtfile in evtfiles:
                log(evtfile, 'Epoching', pcafiles, provenance=customprov)


provenanceParams = [
'tmin',
'tmax',
't_adjust',
'bmin',
'bmax',
'filter_length',
'cont_lp',
'lp_cut',
'proj_sfreq',
'decim',
'drop_thresh',
'bem_type',
'fwd_mindist',
'auto_bad',
'auto_bad_reject',
'auto_bad_flat',
'auto_bad_meg_thresh',
'auto_bad_eeg_thresh',
'ecg_channel',
'eog_channel',
'translate_positions',
'quat_tol',
'tsss_dur',
'mri']


#        self.reject = dict(eog=np.inf, grad=1500e-13, mag=5000e-15, eeg=150e-6)
#        self.flat = dict(eog=-1, grad=1e-13, mag=1e-15, eeg=1e-6)

