#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime
from niprov.commandline import Commandline
from niprov.dependencies import Dependencies


def inspect(fpath, listener=Commandline(), libs=Dependencies()):
    provenance = {}
    if libs.hasDependency('nibabel'):
        img = libs.nibabel.load(fpath)
        provenance['subject'] = img.header.general_info['patient_name']
        provenance['protocol'] = img.header.general_info['protocol_name']
        acqstring = img.header.general_info['exam_date']
        dateformat = '%Y.%m.%d / %H:%M:%S'
        provenance['acquired'] = datetime.strptime(acqstring,dateformat)
    return provenance

    
