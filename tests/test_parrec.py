import unittest
import numpy
from mock import Mock, sentinel
from datetime import datetime
from tests.test_basefile import BaseFileTests


class ParrecTests(BaseFileTests):

    def setUp(self):
        super(ParrecTests, self).setUp()
        self.libs = Mock()
        self.dependencies.getLibraries.return_value = self.libs
        self.setupNibabel()
        from niprov.parrec import ParrecFile
        self.constructor = ParrecFile
        self.file = ParrecFile(self.path, dependencies=self.dependencies)

    def test_Gets_basic_info_from_nibabel_and_returns_it(self):
        out = self.file.inspect()
        self.assertEqual(out['subject'], 'John Doeish')
        self.assertEqual(out['protocol'], 'T1 SENSE')
        self.assertEqual(out['acquired'], datetime(2014, 8, 5, 11, 27, 34))

    def test_Gets_dimensions(self):
        out = self.file.inspect()
        self.assertEqual(out['dimensions'], [80,80,10])

    def test_Gets_advanced_fields(self):
        out = self.file.inspect()
        self.assertEqual(out['technique'], 'T1TFE')
        self.assertEqual(out['repetition-time'], 4.364)
        self.assertEqual(out['field-of-view'], [130., 100., 154.375])
        self.assertEqual(out['epi-factor'], 1)
        self.assertEqual(out['magnetization-transfer-contrast'], False)
        self.assertEqual(out['diffusion'], False)
        self.assertEqual(out['duration'], 65)
        self.assertEqual(out['subject-position'], 'Head First Supine')
        self.assertEqual(out['water-fat-shift'], 1.117)
        # per-image
        self.assertEqual(out['slice-thickness'], 10.0)
        self.assertEqual(out['slice-orientation'], 1)
        self.assertEqual(out['echo-time'], 2.0800000000000001)
        self.assertEqual(out['flip-angle'], 8.0)
        self.assertEqual(out['inversion-time'], 0.0)

    def test_getProtocolFields(self):
        protocol = self.file.getProtocolFields()
        self.assertIn('repetition-time', protocol)
        self.assertIn('echo-time', protocol)

    def test_multiple_TRs(self):
        img = self.libs.nibabel.load.return_value
        img.header.general_info['repetition_time'] = numpy.array([130, 450])
        self.libs.nibabel.load.return_value = img
        out = self.file.inspect()
        self.assertEqual(out['repetition-time'], [130, 450])

    def test_Tells_camera_to_save_snapshot_to_cache(self):
        img = self.libs.nibabel.load.return_value
        data = sentinel.imagedata
        img.get_data.return_value = data
        out = self.file.inspect()
        self.camera.saveSnapshot.assert_called_with(data, for_=self.file)

    def test_Determines_modality(self):
        out = self.file.inspect()
        self.assertEqual(out['modality'], 'MRI')

    def test_Determines_modality_for_diffusion(self):
        img = self.libs.nibabel.load.return_value
        img.header.general_info['diffusion'] = 1
        self.libs.nibabel.load.return_value = img
        out = self.file.inspect()
        self.assertEqual(out['modality'], 'DWI')

    def test_Preserves_modality_if_inherited(self):
        pass # Doesn't have to preserve

    def setupNibabel(self):
        import numpy
        img = Mock()
        img.header.general_info = {
             'acq_nr': 6,
             'angulation': numpy.array([-1.979,  0.546,  0.019]),
             'diffusion': 0,
             'diffusion_echo_time': 0.0,
             'dyn_scan': 0,
             'epi_factor': 1,
             'exam_date': '2014.08.05 / 11:27:34',
             'exam_name': 'test',
             'flow_compensation': 0,
             'fov': numpy.array([ 130.   ,  100.   ,  154.375]),
             'max_cardiac_phases': 1,
             'max_diffusion_values': 1,
             'max_dynamics': 1,
             'max_echoes': 1,
             'max_gradient_orient': 1,
             'max_mixes': 1,
             'max_slices': 10,
             'mtc': 0,
             'nr_label_types': 0,
             'off_center': numpy.array([-18.805,  22.157, -17.977]),
             'patient_name': 'John Doeish',
             'patient_position': 'Head First Supine',
             'phase_enc_velocity': numpy.array([ 0.,  0.,  0.]),
             'prep_direction': 'Right-Left',
             'presaturation': 0,
             'protocol_name': 'T1 SENSE',
             'recon_nr': 1,
             'repetition_time': 4.364,
             'scan_duration': 65.0,
             'scan_mode': '3D',
             'scan_resolution': numpy.array([76, 62]),
             'series_type': 'Image   MRSERIES',
             'spir': 0,
             'tech': 'T1TFE',
             'water_fat_shift': 1.117}
        img.header.image_defs = numpy.array([ (1, 1, 1, 1, 0, 2, 0, 16, 81, [80, 80], 0.0, 1.26032, 2.84925e-05, 133, 231, [-1.98, 0.55, 0.02], [-18.79, -22.82, -16.42], 10.0, 0.0, 0, 1, 0, 2, [1.912, 1.912], 2.08, 0.0, 0.0, 0.0, 1, 8.0, 0, 0, 0, 7, 0.0, 1, 1, '7', '0', [0.0, 0.0, 0.0], 1),
       (2, 1, 1, 1, 0, 2, 1, 16, 81, [80, 80], 0.0, 1.26032, 2.84925e-05, 294, 512, [-1.98, 0.55, 0.02], [-18.79, -12.82, -16.77], 10.0, 0.0, 0, 1, 0, 2, [1.912, 1.912], 2.08, 0.0, 0.0, 0.0, 1, 8.0, 0, 0, 0, 7, 0.0, 1, 1, '7', '0', [0.0, 0.0, 0.0], 1),
       (3, 1, 1, 1, 0, 2, 2, 16, 81, [80, 80], 0.0, 1.26032, 2.84925e-05, 427, 742, [-1.98, 0.55, 0.02], [-18.8, -2.83, -17.11], 10.0, 0.0, 0, 1, 0, 2, [1.912, 1.912], 2.08, 0.0, 0.0, 0.0, 1, 8.0, 0, 0, 0, 7, 0.0, 1, 1, '7', '0', [0.0, 0.0, 0.0], 1)], 
      dtype=[('slice number', '<i8'), ('echo number', '<i8'), ('dynamic scan number', '<i8'), ('cardiac phase number', '<i8'), ('image_type_mr', '<i8'), ('scanning sequence', '<i8'), ('index in REC file', '<i8'), ('image pixel size', '<i8'), ('scan percentage', '<i8'), ('recon resolution', '<i8', (2,)), ('rescale intercept', '<f8'), ('rescale slope', '<f8'), ('scale slope', '<f8'), ('window center', '<i8'), ('window width', '<i8'), ('image angulation', '<f8', (3,)), ('image offcentre', '<f8', (3,)), ('slice thickness', '<f8'), ('slice gap', '<f8'), ('image_display_orientation', '<i8'), ('slice orientation', '<i8'), ('fmri_status_indication', '<i8'), ('image_type_ed_es', '<i8'), ('pixel spacing', '<f8', (2,)), ('echo_time', '<f8'), ('dyn_scan_begin_time', '<f8'), ('trigger_time', '<f8'), ('diffusion_b_factor', '<f8'), ('number of averages', '<i8'), ('image_flip_angle', '<f8'), ('cardiac frequency', '<i8'), ('minimum RR-interval', '<i8'), ('maximum RR-interval', '<i8'), ('TURBO factor', '<i8'), ('Inversion delay', '<f8'), ('diffusion b value number', '<i8'), ('gradient orientation number', '<i8'), ('contrast type', 'S30'), ('diffusion anisotropy type', 'S30'), ('diffusion', '<f8', (3,)), ('label type', '<i8')])
        img.shape = (80,80,10)
        self.libs.nibabel.load.return_value = img
        self.libs.hasDependency.return_value = True




