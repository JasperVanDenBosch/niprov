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
from niprov.discovery import discover


def handler(text, func, out, params):
    """mnefun on_process handler
    """
    for subj in params.subjects:
        subjrawdir = os.path.join(params.work_dir, subj, params.raw_dir)
        discover(subjrawdir)
