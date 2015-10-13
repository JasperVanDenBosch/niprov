import os
from mock import Mock, patch, call
from tests.ditest import DependencyInjectionTestBase


class PipelineTests(DependencyInjectionTestBase):

    def setUp(self):
        super(PipelineTests, self).setUp()

    def test_asFilenameTree(self):
        from niprov.pipeline import Pipeline
        a = self.fileWithLocationAndParents('a:/p/a.f',[])
        b = self.fileWithLocationAndParents('a:/p/c.f',['a:/p/a.f'])
        c = self.fileWithLocationAndParents('b:/c/d/d.f',['a:/p/a.f'])
        d = self.fileWithLocationAndParents('b:/c/d/e.f',['a:/p/c.f'])
        pipelineFiles = [a,b,c,d]
        pipeline = Pipeline(pipelineFiles)
        tree = pipeline.asFilenameTree()
        self.assertEqual({'a.f':{'c.f':{'e.f':{}},'d.f':{}}}, tree)

    def test_Determines_roots_on_creation(self):
        from niprov.pipeline import Pipeline
        b = self.fileWithLocationAndParents('b',['r1','a'])
        r1 = self.fileWithLocationAndParents('r1',[])
        a = self.fileWithLocationAndParents('a',['r2'])
        r2 = self.fileWithLocationAndParents('r2',[])
        pipelineFiles = [a,b,r1,r2]
        pipeline = Pipeline(pipelineFiles)
        self.assertEqual(set([r1,r2]), pipeline.roots)

    def fileWithLocationAndParents(self, loc, parents):
        f = Mock()
        f.location.toString.return_value = loc
        f.provenance = {'parents':parents}
        f.parents = parents
        return f



