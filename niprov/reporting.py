#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.jsonfile import JsonFile
from niprov.exporters import ExportFactory
from niprov.commandline import Commandline


def report(medium=None, form=None, forFile=None, forSubject=None, 
        repository=JsonFile(), exportFactory=ExportFactory(), 
        listener=Commandline()):
    """Publish or simply return provenance for selected files.

    To get provenance on one specific file, pass its path as the 'forFile' 
    argument. Alternatively, to get all files associated with a certain subject,
    use the 'forSubject' argument. If none of these is used, provenance for all
    files is reported.

    Args:
        medium (str): The medium in which to publish the provenance. 
            One of 'html' (save as html and open in firefox),
                'stdout' (print the provenance to the terminal)
        forFile (str): Select one file based on this path.
        forSubject (str): Select files regarding this subject.

    Returns:
        Provenance reported. Either a list of dicts, or a dict.
    """
    exporter = exportFactory.createExporter(medium, form)
    if forFile:
        if not repository.knowsByPath(forFile):
            listener.unknownFile(forFile)
            return
        provenance = repository.byPath(forFile)
    elif forSubject:
        provenance = repository.bySubject(forSubject)
    else:
        provenance = repository.all()
    return exporter.export(provenance)

