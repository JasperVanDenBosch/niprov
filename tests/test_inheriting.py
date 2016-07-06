from tests.ditest import DependencyInjectionTestBase
from mock import Mock, sentinel
from datetime import datetime

class InheritanceTests(DependencyInjectionTestBase):

    def setUp(self):
        super(InheritanceTests, self).setUp()

    def test_InheritFrom(self):
        from niprov.inheriting import inheritFrom
        parentProv = {'acquired':datetime.now(),
            'subject':'JD', 
            'protocol':'X',
            'technique':'abc',
            'repetition-time':1.0,
            'epi-factor':1.0,
            'magnetization-transfer-contrast':True,
            'diffusion':True,
            'echo-time':123,
            'flip-angle':892,
            'inversion-time':123}
        prov = inheritFrom({'a':1}, parentProv)
        self.assertEqual(prov['acquired'], parentProv['acquired'])
        self.assertEqual(prov['subject'], parentProv['subject'])
        self.assertEqual(prov['protocol'], parentProv['protocol'])
        self.assertEqual(prov['technique'], parentProv['technique'])
        self.assertEqual(prov['repetition-time'], parentProv['repetition-time'])
        self.assertEqual(prov['epi-factor'], parentProv['epi-factor'])
        self.assertEqual(prov['magnetization-transfer-contrast'], 
            parentProv['magnetization-transfer-contrast'])
        self.assertEqual(prov['diffusion'], parentProv['diffusion'])
        self.assertEqual(prov['echo-time'], parentProv['echo-time'])
        self.assertEqual(prov['flip-angle'], parentProv['flip-angle'])
        self.assertEqual(prov['inversion-time'], parentProv['inversion-time'])

    def test_Doesnt_complain_if_parent_is_missing_basic_fields(self):
        from niprov.inheriting import inheritFrom
        prov = inheritFrom({'a':1}, {'b':2})

