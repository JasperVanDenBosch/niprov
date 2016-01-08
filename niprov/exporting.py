#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.dependencies import Dependencies


def export(medium=None, form=None, forFile=None, forSubject=None, 
        statistics=False, dependencies=Dependencies()):
    """Publish or simply return provenance for selected files.

    To get provenance on one specific file, pass its path as the 'forFile' 
    argument. Alternatively, to get all files associated with a certain subject,
    use the 'forSubject' argument. If none of these is used, provenance for the 
    most recently registered files is reported.

    Args:
        medium (str): The medium in which to publish the provenance. 
            One of 'stdout' (print the provenance to the terminal) or None.
        forFile (str): Select one file based on this path.
        forSubject (str): Select files regarding this subject.
        statistics (bool): Print overall statistics.

    Returns:
        Provenance reported. Either a list of dicts, or a dict.
    """
    formatFactory = dependencies.getFormatFactory()
    mediumFactory = dependencies.getMediumFactory()
    repository = dependencies.getRepository()
    listener = dependencies.getListener()
    location = dependencies.getLocationFactory()

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
    elif forSubject:
        provenance = repository.bySubject(forSubject)
    else:
        provenance = repository.latest()

    formattedProvenance = form.serialize(provenance)
    return medium.export(formattedProvenance)

