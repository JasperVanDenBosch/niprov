from niprov.dependencies import Dependencies
from niprov.pipeline import Pipeline


class PipelineFactory(object):

    def __init__(self, dependencies=Dependencies()):
        self.files = dependencies.getRepository()

    def forFile(self, image):
        filesByLocation = {image.location.toString():image}

        def lookupParentsRecursive(images):
            parentLocations = set()
            for image in images:
                if 'parents' in image.provenance:
                    parentLocations.update(image.provenance['parents'])
            if len(parentLocations) > 0:
                parents = self.files.byLocations(parentLocations)
                for parent in parents:
                    if not parent.location.toString() in filesByLocation:
                        filesByLocation[parent.location.toString()] = parent
                lookupParentsRecursive(parents)

        lookupParentsRecursive([image])
        return Pipeline(filesByLocation)
