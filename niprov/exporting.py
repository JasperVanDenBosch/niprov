#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.dependencies import Dependencies


def export(provenance, medium, form, pipeline=False, dependencies=Dependencies()):
    """Publish or simply return provenance for selected files.

    To get provenance on one specific file, pass its path as the 'forFile' 
    argument. Alternatively, to get all files associated with a certain subject,
    use the 'forSubject' argument. If none of these is used, provenance for the 
    most recently registered files is reported.

    Args:
        provenance: Niprov BaseFile object or list of such.
        medium (str): The medium in which to publish the provenance. 
            One of:
                'stdout'  (print the provenance to the terminal), 
                'direct'  (return object to caller), 
                'file'    (write to a text file),
                'viewer'  (open in the system image viewer).
        form (str): The format in which to serialize the provenance. 
            One of 'json','xml','narrated','simple','dict','picture'.

    Returns:
        Depends on medium selected. 
    """
    formatFactory = dependencies.getFormatFactory()
    mediumFactory = dependencies.getMediumFactory()
    makePipeline = dependencies.getPipelineFactory()

    form = formatFactory.create(form)
    medium = mediumFactory.create(medium)
    
    if pipeline:
        provenance = makePipeline.forFile(provenance)

    formattedProvenance = form.serialize(provenance)
    return medium.export(formattedProvenance, form)

def print_(provenance, pipeline=False, dependencies=Dependencies()):
    """Shortcut for export(medium='stdout', form='simple').
    """
    return export(provenance, medium='stdout', form='simple',
                  pipeline=pipeline, dependencies=dependencies)

def backup(dependencies=Dependencies()):
    """Shortcut for export(medium='file', form='json') for all provenance.
    """
    provenance = dependencies.getQuery().all()
    return export(provenance, medium='file', form='json', 
                  dependencies=dependencies)

def view(provenance, pipeline=False, dependencies=Dependencies()):
    """Shortcut for export(medium='viewer', form='picture').
    """
    return export(provenance, medium='viewer', form='picture', 
        pipeline=pipeline, dependencies=dependencies)

