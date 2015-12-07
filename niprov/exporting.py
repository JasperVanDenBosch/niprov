from niprov.dependencies import Dependencies
from niprov.jsonfile import JsonFile
from datetime import datetime as dt


def export(dependencies=Dependencies()):
    """Save all current provenance to a file in the current working directory.

    This can serve as a backup, migration tool, or for exchange.
    """
    nowstr = dependencies.getClock().getNowString()
    filepath = 'provenance_export_{0}.json'.format(nowstr)
    repository = dependencies.getRepository()
    exportDeps = Dependencies()
    exportDeps.getConfiguration().database_url = filepath
    exportRepo = JsonFile(exportDeps)
    allFiles = repository.all()
    for pfile in allFiles:
        exportRepo.add(pfile)
    return filepath


def importp(filepath, dependencies=Dependencies()):
    """Add provenance in bulk from a file, such as saved by export().

    Named importp as opposed to import because the latter is a reserved word
    in Python.

    This can serve as a backup, migration tool, or for exchange.
    """
    repository = dependencies.getRepository()
    importDeps = Dependencies()
    importDeps.getConfiguration().database_url = filepath
    importRepo = JsonFile(importDeps)
    allFiles = importRepo.all()
    for pfile in allFiles:
        repository.add(pfile)
