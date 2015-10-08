import os
from mock import Mock, patch, call, sentinel
from tests.ditest import DependencyInjectionTestBase


class PipelineFactoryTests(DependencyInjectionTestBase):

    def setUp(self):
        super(PipelineFactoryTests, self).setUp()

    def test_forFile_returns_Pipeline(self):
        from niprov.pipelinefactory import PipelineFactory
        from niprov.pipeline import Pipeline
        factory = PipelineFactory(dependencies=self.dependencies)
        target = Mock()
        target.provenance = {}
        pipeline = factory.forFile(target)
        self.assertIsInstance(pipeline, Pipeline)

    def test_forFile_makes_pipeline_with_targets_parents(self):
        from niprov.pipelinefactory import PipelineFactory
        p1a = self.fileWithLocation('p1a')
        p1b = self.fileWithLocation('p1b')
        t = self.fileWithLocation('t')
        self.repo.byLocations.side_effect = lambda l: [p1a, p1b]
        factory = PipelineFactory(dependencies=self.dependencies)
        t.provenance['parents'] = ['p1a','p1b']
        with patch('niprov.pipelinefactory.Pipeline') as PipelineCtr:
            pipeline = factory.forFile(t)
            self.repo.byLocations.assert_called_with(['p1a','p1b'])
            PipelineCtr.assert_called_with({'p1a':{'t':{}},'p1b':{'t':{}}},
                {'t':t,'p1a':p1a,'p1b':p1b})

    def fileWithLocation(self, loc):
        f = Mock()
        f.location.toString.return_value = loc
        f.provenance = {}
        return f




