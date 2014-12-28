#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
from datetime import datetime
from niprov.commandline import Commandline
from niprov.dependencies import Dependencies

formats = {'.PAR':'nibabel',
           '.dcm':'dicom'}


def inspect(fpath, listener=Commandline(), libs=Dependencies()):
    provenance = {}
    extension = os.path.splitext(fpath)[1]
    if not extension in formats:
        errmsg = 'Image file with extension {0} not supported.'
        raise ValueError(errmsg.format(extension))
    if not libs.hasDependency(formats[extension]):
        listener.missingDependencyForImage(formats[extension], fpath)
        return None
    if formats[extension] == 'nibabel':
        try:
            img = libs.nibabel.load(fpath)
        except:
            listener.fileError(fpath)
            return None
        provenance['subject'] = img.header.general_info['patient_name']
        provenance['protocol'] = img.header.general_info['protocol_name']
        acqstring = img.header.general_info['exam_date']
        dateformat = '%Y.%m.%d / %H:%M:%S'
        provenance['acquired'] = datetime.strptime(acqstring,dateformat)
    if formats[extension] == 'dicom':
        try:
            img = libs.dicom.read_file(fpath)
        except:
            listener.fileError(fpath)
            return None
        provenance['subject'] = img.PatientID
        provenance['protocol'] = img.SeriesDescription
        acqstring = img.AcquisitionDateTime.split('.')[0]
        dateformat = '%Y%m%d%H%M%S'
        provenance['acquired'] = datetime.strptime(acqstring,dateformat)
    return provenance


    
