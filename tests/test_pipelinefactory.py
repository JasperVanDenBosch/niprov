import os
from mock import Mock, patch, call
from tests.ditest import DependencyInjectionTestBase


class PipelineFactoryTests(DependencyInjectionTestBase):

    def setUp(self):
        super(PipelineFactoryTests, self).setUp()

    def test_forFile(self):
        from niprov.pipelinefactory import PipelineFactory
        from niprov.pipeline import Pipeline
        factory = PipelineFactory(dependencies=self.dependencies)
        target = Mock()
        pipeline = factory.forFile(target)
        self.assertIsInstance(pipeline, Pipeline)



