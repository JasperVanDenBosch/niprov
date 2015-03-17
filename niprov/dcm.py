from datetime import datetime, time
from niprov.basefile import BaseFile
from niprov.dependencies import Dependencies


class DicomFile(BaseFile):

    def __init__(self, fpath, dependencies=Dependencies(), **kwargs):
        super(DicomFile, self).__init__(fpath, **kwargs)
        self.libs = dependencies

    def inspect(self):
        """
        Inspect the DICOM file attributes.

        If a general AcquisitionDateTime attribute is not present, the 
        SeriesDate and SeriesTime will be used to set the :ref:`field-acquired` 
        provenance field.

        Returns:
            dict: Provenance for the inspected file.
        """
        provenance = super(DicomFile, self).inspect()
        img = self.libs.dicom.read_file(self.path)
        provenance['subject'] = img.PatientID
        provenance['protocol'] = img.SeriesDescription
        provenance['seriesuid'] = img.SeriesInstanceUID
        provenance['filesInSeries'] = [self.path]
        if hasattr(img, 'NumberOfFrames'):
            provenance['multiframeDicom'] = True
            nframes = int(img.NumberOfFrames)
        else:
            provenance['multiframeDicom'] = False
            nframes = len(provenance['filesInSeries'])
        if hasattr(img, 'Rows'):
            provenance['dimensions'] = [int(img.Rows), int(img.Columns), 
                nframes]
        if hasattr(img, 'AcquisitionDateTime'):
            acqstring = img.AcquisitionDateTime.split('.')[0]
            dateformat = '%Y%m%d%H%M%S'
            provenance['acquired'] = datetime.strptime(acqstring,dateformat)
        else:
            dateformat = '%Y%m%d'
            acqdate = datetime.strptime(img.SeriesDate, dateformat)
            acqtime = datetime.fromtimestamp(float(img.SeriesTime)).time()
            combined = datetime.combine(acqdate, acqtime)
            provenance['acquired'] = combined.replace(microsecond=0)
        return provenance


    def getSeriesId(self):
        """
        Return the DICOM "SeriesInstanceUID" that all files in this series 
        have in common.

        Returns:
            str: A string uniquely identifying files belonging to this series.
        """
        if not hasattr(self, 'provenance'):
            self.inspect()
        return self.provenance['seriesuid']

    def addFile(self, img):
        """
        Add a single DICOM file object to this series.

        The file will be stored in provenance in the 'filesInSeries' list.
        """
        self.provenance['filesInSeries'].append(img.path)
        self._updateNfilesDependentFields()

    def _updateNfilesDependentFields(self):
        if (not self.provenance['multiframeDicom']) and 'dimensions' in self.provenance:
            nfiles = len(self.provenance['filesInSeries'])
            self.provenance['dimensions'][2] = nfiles
        
        
