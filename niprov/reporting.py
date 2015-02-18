#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.jsonfile import JsonFile
from niprov.exporters import ExportFactory
from niprov.commandline import Commandline


def report(format=None, forFile=None, forSubject=None, 
        repository=JsonFile(), exportFactory=ExportFactory(), 
        listener=Commandline()):
    """Publish or simply return provenance for selected files.

    To get provenance on one specific file, pass its path as the 'forFile' 
    argument. Alternatively, to get all files associated with a certain subject,
    use the 'forSubject' argument. If none of these is used, provenance for all
    files is reported.

    Args:
        format (str): The format in which to publish the provenance. 
            Currently only 'html'.
        forFile (str): Select one file based on this path.
        forSubject (str): Select files regarding this subject.

    Returns:
        Provenance reported. Either a list of dicts, or a dict.
    """
    exporter = exportFactory.createExporter(format)
    if forFile:
        if not repository.knowsByPath(forFile):
            listener.unknownFile(forFile)
            return
        provenance = repository.byPath(forFile)
        exporter.export(provenance)
    elif forSubject:
        provenance = repository.bySubject(forSubject)
        exporter.exportList(provenance)
    else:
        provenance = repository.all()
        exporter.exportList(provenance)
    return provenance
