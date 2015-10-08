from niprov.dependencies import Dependencies
from niprov.pipeline import Pipeline


class PipelineFactory(object):

    def __init__(self, dependencies=Dependencies()):
        pass

    def forFile(self, image):
        return Pipeline()
