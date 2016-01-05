from tests.ditest import DependencyInjectionTestBase
from mock import Mock
from datetime import datetime

class BaseFileTests(DependencyInjectionTestBase):

    def setUp(self):
        super(BaseFileTests, self).setUp()
        self.path = 'example.abc'
        self.location.toDictionary.return_value = {'path':self.path}
        from niprov.basefile import BaseFile
        self.constructor = BaseFile
        self.file = BaseFile(self.path, dependencies=self.dependencies)

    def test_Saves_file_path_along_with_provenance(self):
        out = self.file.inspect()
        self.assertEqual(out['path'], self.path)

    def test_Saves_filesize_along_with_provenance(self):
        out = self.file.inspect()
        self.assertEqual(out['size'], self.filesys.getsize(self.path))

    def test_Saves_file_creation_time_along_with_provenance(self):
        out = self.file.inspect()
        self.assertEqual(out['created'], self.filesys.getctime(self.path))

    def test_Asks_hasher_for_digest_of_file(self):
        out = self.file.inspect()
        self.assertEqual(out['hash'], self.hasher.digest(self.path))

    def test_Provenance_property_equals_dictionary_returned_by_inspect(self):
        out = self.file.inspect()
        self.assertEqual(out, self.file.provenance)

    def test_Attach_method(self):
        pass

    def test_Series_interface(self):
        self.assertEqual(self.file.getSeriesId(), None)

    def test_Construct_with_provenance(self):
        prov = {'aprop':'aval'}
        img = self.constructor(self.path, provenance=prov, dependencies=self.dependencies)
        self.assertEqual(prov, img.provenance)

    def test_Construct_with_provenance_adds_path_if_not_set(self):
        prov = {'aprop':'aval'}
        img = self.constructor(self.path, provenance=prov, dependencies=self.dependencies)
        self.assertIn('path', img.provenance)
        self.assertEqual(self.path, img.provenance['path'])

    def test_Inspect_leaves_existing_fields_updates_others(self):
        prov = {'aprop':'aval','size':9876}
        img = self.constructor(self.path, provenance=prov, 
            dependencies=self.dependencies)
        img.inspect()
        self.assertEqual(img.provenance['aprop'], 'aval')
        self.assertEqual(img.provenance['size'], self.filesys.getsize(self.path))

    def test_Uses_location_objects_to_add_location_info_to_provenance(self):
        self.location.toDictionary.return_value = {'newLocKey':'newLocValue',
            'path':'newPathVal'}
        img = self.constructor(self.path, dependencies=self.dependencies)
        self.locationFactory.fromString.assert_called_with(self.path)
        self.assertEqual('newLocValue', img.provenance['newLocKey'])
        self.assertEqual('newPathVal', img.provenance['path'])
        self.assertEqual(self.location, img.location)

    def test_parents_property(self):
        prov = {'aprop':'aval','size':9876}
        img = self.constructor(self.path, provenance=prov, 
            dependencies=self.dependencies)
        self.assertEqual(img.parents, [])
        prov = {'aprop':'aval','parents':['foo','bar']}
        img2 = self.constructor(self.path, provenance=prov, 
            dependencies=self.dependencies)
        self.assertEqual(img2.parents, ['foo','bar'])

    def test_getProvenance_provides_prov_serialized_in_requested_format(self):
        img = self.constructor(self.path, dependencies=self.dependencies)
        out = img.getProvenance('myformat')
        self.formatFactory.create.assert_called_with('myformat')
        self.format.serialize.assert_called_with(img)
        self.assertEqual(self.format.serialize(), out)

