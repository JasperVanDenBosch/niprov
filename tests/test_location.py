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

    def test_Location_toUrl(self):
        from niprov.location import Location
        loc = Location('HAL:/p/n1.f')
        expected = 'file://HAL/p/n1.f'
        self.assertEqual(expected, loc.toUrl())

    def test_Location_makes_relative_paths_absolute(self):
        from niprov.location import Location
        with patch('niprov.location.socket') as socket:
            socket.gethostname.return_value = 'HAL'
            with patch('niprov.location.os.path') as ospath:
                ospath.abspath.return_value = '/absolute/path'
                loc = Location('relative/path')
                self.assertEqual('/absolute/path', loc.path)
                self.assertEqual('HAL:/absolute/path', str(loc))
                loc = Location('KITT:relative/path')
                self.assertEqual('/absolute/path', loc.path)
                self.assertEqual('KITT:/absolute/path', str(loc))

    def test_location_equals(self):
        from niprov.location import Location
        loc1 = Location('relative/path')
        loc2 = Location('relative/path')
        loc3 = Location('relative/other/path')
        self.assertEqual(loc1, loc2)
        self.assertNotEqual(loc1, loc3)

