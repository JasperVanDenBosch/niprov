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
from niprov.commandline import Commandline
from niprov.dependencies import Dependencies
from niprov.discovery import discover
from niprov.logging import log


def handler(text, func, out, params, listener=Commandline(), 
    libs=Dependencies()):
    """mnefun on_process handler
    """
    funcname = func.func_name
    listener.mnefunEventReceived(funcname)
    for subj in params.subjects:
        if funcname == 'fetch_raw_files':
            subjrawdir = os.path.join(params.work_dir, subj, params.raw_dir)
            discover(subjrawdir)
        elif funcname == 'fetch_sss_files':
            rawfiles = libs.mnefun.get_raw_fnames(params, subj, 'raw')
            sssfiles = libs.mnefun.get_raw_fnames(params, subj, 'sss')
            for rawfile, sssfile in zip(rawfiles, sssfiles):
                log(sssfile, 'Signal Space Separation', rawfile)
        elif funcname == 'apply_preprocessing_combined':
            sssfiles = libs.mnefun.get_raw_fnames(params, subj, 'sss')
            pcafiles = libs.mnefun.get_raw_fnames(params, subj, 'pca')
            for sssfile, pcafile in zip(sssfiles, pcafiles):
                log(pcafile, 'Signal Space Projection', sssfile)
        elif funcname == 'save_epochs':
            pcafiles = libs.mnefun.get_raw_fnames(params, subj, 'pca')
            evtfiles = libs.mnefun._paths.get_epochs_evokeds_fnames(params, 
                subj, params.analyses)
            for evtfile in evtfiles:
                log(evtfile, 'Epoching', pcafiles)

