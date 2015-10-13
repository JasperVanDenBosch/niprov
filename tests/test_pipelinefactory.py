import os
from mock import Mock, patch, call, sentinel
from tests.ditest import DependencyInjectionTestBase


class PipelineFactoryTests(DependencyInjectionTestBase):

    def setUp(self):
        super(PipelineFactoryTests, self).setUp()

#    def test_forFile_returns_Pipeline(self):
#        from niprov.pipelinefactory import PipelineFactory
#        from niprov.pipeline import Pipeline
#        self.repo.byLocations.return_value = []
#        factory = PipelineFactory(dependencies=self.dependencies)
#        target = Mock()
#        target.provenance = {}
#        pipeline = factory.forFile(target)
#        self.assertIsInstance(pipeline, Pipeline)

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
        self.repo.byParents.side_effect = lambda ls: []
        factory = PipelineFactory(dependencies=self.dependencies)
        with patch('niprov.pipelinefactory.Pipeline') as PipelineCtr:
            pipeline = factory.forFile(t)
            PipelineCtr.assert_called_with(repodict.values())
            self.assertEqual(3, self.repo.byLocations.call_count)
            self.assertEqual(1, self.repo.byParents.call_count)

    def test_forFile_makes_pipeline_with_targets_children(self):
        from niprov.pipelinefactory import PipelineFactory
        c1a = self.fileWithLocation('c1a')
        c1b = self.fileWithLocation('c1b')
        c2a = self.fileWithLocation('c2a')
        c2b = self.fileWithLocation('c2b')
        c1a.provenance['parents'] = ['t']
        c1b.provenance['parents'] = ['t']
        c2a.provenance['parents'] = ['c1a']
        c2b.provenance['parents'] = ['c1a','c1b']
        t = self.fileWithLocation('t')
        repodict = {'t':t,'c1a':c1a, 'c1b':c1b, 'c2a':c2a, 'c2b':c2b}
        childrenByParent = {'t':[c1a, c1b],'c1a':[c2a],'c1b':[c2a, c2b],
            'c2a':[],'c2b':[]}
        self.repo.byLocations.side_effect = lambda ls: []
        self.repo.byParents.side_effect = lambda ps: [c for p in ps for c in childrenByParent[p]]
        factory = PipelineFactory(dependencies=self.dependencies)
        with patch('niprov.pipelinefactory.Pipeline') as PipelineCtr:
            pipeline = factory.forFile(t)
            PipelineCtr.assert_called_with(repodict.values())
            self.assertEqual(1, self.repo.byLocations.call_count)
            self.assertEqual(3, self.repo.byParents.call_count)

    def test_forFile_should_call_repo_with_list_not_set(self):
        from niprov.pipelinefactory import PipelineFactory
        p1a = self.fileWithLocation('p1a')
        p1b = self.fileWithLocation('p1b')
        t = self.fileWithLocation('t')
        t.provenance['parents'] = ['p1a','p1b']
        repodict = {'t':t,'p1a':p1a, 'p1b':p1b}
        self.repo.byLocations.side_effect = lambda ls: [repodict[l] for l in ls]
        self.repo.byParents.side_effect = lambda ls: []
        factory = PipelineFactory(dependencies=self.dependencies)
        with patch('niprov.pipelinefactory.Pipeline') as PipelineCtr:
            pipeline = factory.forFile(t)
            self.repo.byLocations.assert_called_with([])
            self.repo.byLocations.assert_any_call(['p1a','p1b'])

    def fileWithLocation(self, loc):
        f = Mock()
        f.location.toString.return_value = loc
        f.provenance = {}
        return f






