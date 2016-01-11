#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.dependencies import Dependencies


def export(medium, form, forFile=None, forSubject=None, 
        statistics=False, pipeline=False, dependencies=Dependencies()):
    """Publish or simply return provenance for selected files.

    To get provenance on one specific file, pass its path as the 'forFile' 
    argument. Alternatively, to get all files associated with a certain subject,
    use the 'forSubject' argument. If none of these is used, provenance for the 
    most recently registered files is reported.

    Args:
        medium (str): The medium in which to publish the provenance. 
            One of 'stdout' (print the provenance to the terminal), 'direct' 
            (return object to caller), or 'file' (write to a text file).
        form (str): The format in which to serialize the provenance. 
            One of 'json','xml','narrated','simple','dict'.
        forFile (str): Select one file based on this path.
        forSubject (str): Select files regarding this subject.
        statistics (bool): Print overall statistics.

    Returns:
        Depends on medium selected. 
    """
    formatFactory = dependencies.getFormatFactory()
    mediumFactory = dependencies.getMediumFactory()
    repository = dependencies.getRepository()
    listener = dependencies.getListener()
    location = dependencies.getLocationFactory()
    makePipeline = dependencies.getPipelineFactory()

    form = formatFactory.create(form)
    medium = mediumFactory.create(medium)
    
    if statistics:
        provenance = repository.statistics()
    elif forFile:
        forFile = location.completeString(forFile)
        if not repository.knowsByLocation(forFile):
            listener.unknownFile(forFile)
            return
        provenance = repository.byLocation(forFile)
        if pipeline:
            provenance = makePipeline.forFile(provenance)
    elif forSubject:
        provenance = repository.bySubject(forSubject)
    else:
        provenance = repository.latest()

    formattedProvenance = form.serialize(provenance)
    return medium.export(formattedProvenance)


def get(forFile=None, forSubject=None, statistics=False, pipeline=False, 
    dependencies=Dependencies()):
    """Shortcut for export(medium='direct', form='object').
    """
    return export(medium='direct', form='object', 
        forFile=forFile, forSubject=forSubject, statistics=statistics, 
        pipeline=pipeline, dependencies=dependencies)

def print_(forFile=None, forSubject=None, statistics=False, pipeline=False, 
    dependencies=Dependencies()):
    """Shortcut for export(medium='stdout', form='simple').
    """
    return export(medium='stdout', form='simple', 
        forFile=forFile, forSubject=forSubject, statistics=statistics, 
        pipeline=pipeline, dependencies=dependencies)

def backup(dependencies=Dependencies()):
    """Shortcut for export(medium='file', form='json') for all provenance.
    """
    return export(medium='file', form='json', dependencies=dependencies)

