from mock import Mock, patch, sentinel
from tests.ditest import DependencyInjectionTestBase
import datetime


class ClockTest(DependencyInjectionTestBase):

    def setUp(self):
        super(ClockTest, self).setUp()

    def test_Can_create_datetimestring(self):
        from niprov.clock import Clock
        now = datetime.datetime(year=1982, month=1, day=2, 
            hour=3, minute=4, second=5, microsecond=6789)
        with patch('niprov.clock.datetime') as datetimeModule:
            datetimeModule.datetime.now.return_value = now
            klok = Clock()
            self.assertEqual(klok.getNowString(), '1982-01-02_03-04-05')



