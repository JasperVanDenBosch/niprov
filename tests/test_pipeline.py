import os
from mock import Mock, patch, call
from tests.ditest import DependencyInjectionTestBase


class PipelineTests(DependencyInjectionTestBase):

    def setUp(self):
        super(PipelineTests, self).setUp()

    def test_asFilenameTree(self):
        from niprov.pipeline import Pipeline
        inner = {'a:/p/c.f':{'b:/c/d/e.f':{}},'b:/c/d/d.f':{}}
        locTree = {'a:/p/a.f':inner,'a:/p/b.f':{}}
        pipeline = Pipeline({})
        pipeline.locationTree = locTree
        tree = pipeline.asFilenameTree()
        self.assertEqual({'a.f':{'c.f':{'e.f':{}},'d.f':{}},'b.f':{}}, tree)



