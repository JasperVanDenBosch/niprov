from datetime import datetime
from niprov.basefile import BaseFile
from niprov.libraries import Libraries


class ParrecFile(BaseFile):

    def __init__(self, location, **kwargs):
        super(ParrecFile, self).__init__(location, **kwargs)
        self.libs = self.dependencies.getLibraries()

    def inspect(self):
        provenance = super(ParrecFile, self).inspect()
        img = self.libs.nibabel.load(self.path)
        info = img.header.general_info
        provenance['dimensions'] = list(img.shape)
        dateformat = '%Y.%m.%d / %H:%M:%S'
        acqstring = info['exam_date']
        provenance['acquired'] = datetime.strptime(acqstring, dateformat)
        provenance['subject'] = info['patient_name']
        provenance['protocol'] = info['protocol_name']
        provenance['technique'] = info['tech']
        provenance['repetition-time'] = info['repetition_time']
        provenance['field-of-view'] = info['fov'].tolist()
        provenance['epi-factor'] = info['epi_factor']
        provenance['magnetization-transfer-contrast'] = bool(info['mtc'])
        provenance['diffusion'] = bool(info['diffusion'])
        # per-image
        img0info = img.header.image_defs[0]
        provenance['slice-thickness'] = img0info['slice thickness']
        provenance['slice-orientation'] = img0info['slice orientation']
        provenance['echo-time'] = img0info['echo_time']
        provenance['flip-angle'] = img0info['image_flip_angle']
        provenance['inversion-time'] = img0info['Inversion delay']
        return provenance
