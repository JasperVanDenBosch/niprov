from niprov.dependencies import Dependencies
from niprov.jsonfile import JsonFile


def export(dependencies=Dependencies()):
    """Save all current provenance to a file in the current working directory.

    This can serve as a backup, migration tool, or for exchange.
    """
    exportDeps = Dependencies()
    exportDeps.getConfiguration().database_url = 'provenance.json'
    exportRepo = JsonFile(exportDeps)
    allFiles = dependencies.getRepository().all()
    for pfile in allFiles:
        exportRepo.add(pfile)


def importp(filepath, dependencies=Dependencies()):
    """Add provenance in bulk from a file, such as saved by export().

    This can serve as a backup, migration tool, or for exchange.
    """
    pass
