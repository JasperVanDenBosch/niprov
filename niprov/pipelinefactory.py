from niprov.dependencies import Dependencies
from niprov.pipeline import Pipeline


class PipelineFactory(object):

    def __init__(self, dependencies=Dependencies()):
        self.files = dependencies.getRepository()

    def forFile(self, image):
        """Create a Pipeline object based on known files 'parents' field.
        """
        filesByLocation = {image.location.toString():image}

        def lookupRelativesRecursive(images, relationToLookFor):
            if relationToLookFor is 'parents':
                parentLocations = set()
                for image in images:
                    parentLocations.update(image.provenance.get('parents',[]))
                relatives = self.files.byLocations(list(parentLocations))
            elif relationToLookFor is 'children':
                thisGenerationLocations = [i.location.toString() for i in images]
                relatives = self.files.byParents(thisGenerationLocations)
            for relative in relatives:
                filesByLocation[relative.location.toString()] = relative
            if relatives:
                lookupRelativesRecursive(relatives, relationToLookFor)

        lookupRelativesRecursive([image], 'parents')
        lookupRelativesRecursive([image], 'children')
        return Pipeline(filesByLocation.values())
