from mock import Mock, patch
from tests.ditest import DependencyInjectionTestBase


class LocationTests(DependencyInjectionTestBase):

    def setUp(self):
        super(LocationTests, self).setUp()

    def test_LocationFactory_fromString(self):
        from niprov.locationfactory import LocationFactory
        with patch('niprov.locationfactory.Location') as Location:
            factory = LocationFactory()
            out = factory.fromString('abc')
            Location.assert_called_with('abc')
            self.assertEqual(Location(), out)

    def test_Location_toDictionary(self):
        from niprov.location import Location
        loc = Location('/p/n1.f')
        self.assertEqual({'path':'/p/n1.f'}, loc.toDictionary())


