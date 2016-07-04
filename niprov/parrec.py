from datetime import datetime
import numpy
from niprov.basefile import BaseFile
from niprov.libraries import Libraries


class ParrecFile(BaseFile):

    def __init__(self, location, **kwargs):
        super(ParrecFile, self).__init__(location, **kwargs)
        self.libs = self.dependencies.getLibraries()
        self.camera = self.dependencies.getCamera()

    def inspect(self):
        provenance = super(ParrecFile, self).inspect()
        img = self.libs.nibabel.load(self.path)
        info = img.header.general_info
        provenance['dimensions'] = list(img.shape)
        dateformat = '%Y.%m.%d / %H:%M:%S'
        acqstring = info['exam_date']
        provenance['acquired'] = datetime.strptime(acqstring, dateformat)
        provenance['subject'] = info['patient_name']
        provenance['subject-position'] = info['patient_position']
        provenance['protocol'] = info['protocol_name']
        provenance['technique'] = info['tech']
        tr = info['repetition_time']
        if isinstance(tr, numpy.ndarray):
            tr = tr.tolist()
        provenance['repetition-time'] = tr
        provenance['field-of-view'] = info['fov'].tolist()
        provenance['epi-factor'] = info['epi_factor']
        provenance['magnetization-transfer-contrast'] = bool(info['mtc'])
        provenance['diffusion'] = bool(info['diffusion'])
        provenance['duration'] = info['scan_duration']
        provenance['water-fat-shift'] = info['water_fat_shift']
        # per-image
        img0info = img.header.image_defs[0]
        provenance['slice-thickness'] = img0info['slice thickness']
        provenance['slice-orientation'] = img0info['slice orientation']
        provenance['echo-time'] = img0info['echo_time']
        provenance['flip-angle'] = img0info['image_flip_angle']
        provenance['inversion-time'] = img0info['Inversion delay']
        if provenance['diffusion']:
            provenance['modality'] = 'DWI'
        else:
            provenance['modality'] = 'MRI'
        self.camera.saveSnapshot(img.get_data(), for_=self)
        return provenance

    def getProtocolFields(self):
        return ['repetition-time', 'echo-time', 'flip-angle', 'epi-factor', 
                'water-fat-shift', 'subject-position']

