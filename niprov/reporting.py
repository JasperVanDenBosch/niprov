#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.jsonfile import JsonFile
from niprov.exporters import ExportFactory


def report(format=None, forFile=None, forSubject=None, repository=JsonFile(), 
        exportFactory=ExportFactory()):
    exporter = exportFactory.createExporter(format)
    if forFile:
        provenance = repository.byPath(forFile)
        exporter.export(provenance)
    elif forSubject:
        provenance = repository.bySubject(forSubject)
        exporter.exportList(provenance)
    else:
        provenance = repository.all()
        exporter.exportList(provenance)
    return provenance
