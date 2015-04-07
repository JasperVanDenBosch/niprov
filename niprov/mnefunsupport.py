# -*- coding: utf-8 -*-
"""mnefun support module

This module provides handlers to attach to mnefun events.

::

    import mnefun
    import niprov.mnefun
    params = mnefun.Params()
    params.on_process = niprov.mnefun.handler

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
    if funcname == 'fetch_raw_files':
        for subj in params.subjects:
            subjrawdir = os.path.join(params.work_dir, subj, params.raw_dir)
            discover(subjrawdir)
    elif funcname == 'fetch_sss_files':
        for subj in params.subjects:
            rawfiles = libs.mnefun.get_raw_fnames(params, subj, 'raw')
            sssfiles = libs.mnefun.get_raw_fnames(params, subj, 'sss')
            for rawfile, sssfile in zip(rawfiles, sssfiles):
                log(sssfile, 'Signal Space Separation', rawfile)
