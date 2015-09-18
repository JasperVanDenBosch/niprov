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
        loc = Location('HAL:/p/n1.f')
        expected = {'path':'/p/n1.f','hostname':'HAL','location':'HAL:/p/n1.f'}
        self.assertEqual(expected, loc.toDictionary())

    def test_Location_by_default_fills_in_local_hostname(self):
        from niprov.location import Location
        with patch('niprov.location.socket') as socket:
            loc = Location('/p/n1.f')
            self.assertEqual(socket.gethostname(), loc.hostname)

    def test_Location_parses_locationString(self):
        from niprov.location import Location
        with patch('niprov.location.socket') as socket:
            loc = Location('HAL:/p/n1.f')
            self.assertEqual('HAL', loc.hostname)
            self.assertEqual('/p/n1.f', loc.path)

    def test_Location_stringifies_to_full_locationString(self):
        from niprov.location import Location
        with patch('niprov.location.socket') as socket:
            loc = Location('HAL:/p/n1.f')
            self.assertEqual('HAL:/p/n1.f', str(loc))

    def test_LocationFactory_completeString(self):
        from niprov.locationfactory import LocationFactory
        with patch('niprov.locationfactory.Location') as Location:
            factory = LocationFactory()
            factory.fromString = Mock()
            outstr = factory.completeString('/j/k/l')
            factory.fromString.assert_called_with('/j/k/l')
            self.assertEqual(str(factory.fromString()), outstr)

