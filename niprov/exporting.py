from niprov.dependencies import Dependencies
from niprov.jsonfile import JsonFile


def export(dependencies=Dependencies()):
    exportDeps = Dependencies()
    exportDeps.getConfiguration().database_url = 'provenance.json'
    exportRepo = JsonFile(exportDeps)
    allFiles = dependencies.getRepository().all()
    exportRepo.addMany(allFiles)


def importp(filepath, dependencies=Dependencies()):
    pass
