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

    def test_forFile_makes_pipeline_with_targets_parents_parents(self):
        from niprov.pipelinefactory import PipelineFactory
        p1a = self.fileWithLocation('p1a')
        p1b = self.fileWithLocation('p1b')
        p2a = self.fileWithLocation('p2a')
        p2b = self.fileWithLocation('p2b')
        p1a.provenance['parents'] = ['p2a']
        p1b.provenance['parents'] = ['p2a','p2b']
        t = self.fileWithLocation('t')
        t.provenance['parents'] = ['p1a','p1b']
        repodict = {'t':t,'p1a':p1a, 'p1b':p1b, 'p2a':p2a, 'p2b':p2b}
        self.repo.byLocations.side_effect = lambda ls: [repodict[l] for l in ls]
        factory = PipelineFactory(dependencies=self.dependencies)
        with patch('niprov.pipelinefactory.Pipeline') as PipelineCtr:
            pipeline = factory.forFile(t)
            PipelineCtr.assert_called_with(repodict)
            self.assertEqual(2, self.repo.byLocations.call_count)

    def fileWithLocation(self, loc):
        f = Mock()
        f.location.toString.return_value = loc
        f.provenance = {}
        return f






