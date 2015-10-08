from niprov.dependencies import Dependencies
from niprov.pipeline import Pipeline


class PipelineFactory(object):

    def __init__(self, dependencies=Dependencies()):
        self.files = dependencies.getRepository()

    def forFile(self, image):
        filesByLocation = {image.location:image}
        locationTree = {}
        if 'parents' in image.provenance:
            parentLocations = image.provenance['parents']
            for parentLocation in parentLocations:
                locationTree[parentLocation] = {image.location:{}}
            parents = self.files.byLocations(parentLocations)
            for parent in parents:
                if not parent.location in filesByLocation:
                    filesByLocation[parent.location] = parent
        return Pipeline(locationTree, filesByLocation)
