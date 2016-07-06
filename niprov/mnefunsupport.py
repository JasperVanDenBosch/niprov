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
from niprov import ProvenanceContext


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
    provenance = ProvenanceContext()
    funcname = func.func_name
    listener.mnefunEventReceived(funcname)
    paramdict = {}
    for paramname in dir(params):
        objectvalue = getattr(params, paramname)
        blacklist = ['get_projs_from', 'inv_runs']
        if hasattr(objectvalue, '__call__'):
            continue
        if paramname[0] == '_':
            continue
        if 'array' in str(type(objectvalue)):
            continue
        if paramname in blacklist:
            continue
        paramdict[paramname] = objectvalue
    subjects = [params.subjects[i] for i in params.subject_indices]
    for subj in subjects:
        customprov = {'mnefun':paramdict}
        if funcname in ['fetch_raw_files', 'score_fun', 'fetch_sss_files']:
            rawfiles = libs.mnefun.get_raw_fnames(params, subj, 'raw', add_splits=True,
                                                  run_indices=params.subject_run_indices)
        if funcname == 'fetch_raw_files':
            for f in rawfiles:
                provenance.add(f, provenance=customprov)
        elif funcname == 'score_fun':
            eventfiles = libs.mnefun._paths.get_event_fnames(params, subj,
                                                             params.subject_run_indices)
            for rawfile, eventfile in zip(rawfiles, eventfiles):
                provenance.log(eventfile, 'scoring', rawfile, provenance=customprov)
        elif funcname == 'fetch_sss_files':
            trans = 'Signal Space Separation'
            sssfiles = libs.mnefun.get_raw_fnames(params, subj, 'sss')
            for rawfile, sssfile in zip(rawfiles, sssfiles):
                provenance.log(sssfile, trans, rawfile, provenance=customprov)
        elif funcname == 'apply_preprocessing_combined':
            trans = 'Signal Space Projection'
            sssfiles = libs.mnefun.get_raw_fnames(params, subj, 'sss')
            pcafiles = libs.mnefun.get_raw_fnames(params, subj, 'pca')
            for sssfile, pcafile in zip(sssfiles, pcafiles):
                provenance.log(pcafile, trans, sssfile, provenance=customprov)
        elif funcname == 'save_epochs':
            pcafiles = libs.mnefun.get_raw_fnames(params, subj, 'pca')
            evtfiles = libs.mnefun._paths.get_epochs_evokeds_fnames(params, 
                subj, params.analyses)
            for evtfile in evtfiles:
                if os.path.isfile(evtfile[0]):
                    provenance.log(evtfile[0], 'Epoching', pcafiles, provenance=customprov)


#        self.reject = dict(eog=np.inf, grad=1500e-13, mag=5000e-15, eeg=150e-6)
#        self.flat = dict(eog=-1, grad=1e-13, mag=1e-15, eeg=1e-6)
