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
        SeriesDate and SeriesTime will be used to set the 'acquired' 
        provenance field.

        Returns:
            dict: Provenance for the inspected file.
        """
        provenance = super(DicomFile, self).inspect()
        try:
            img = self.libs.dicom.read_file(self.path)
        except:
            self.listener.fileError(self.path)
            return provenance
        provenance['subject'] = img.PatientID
        provenance['protocol'] = img.SeriesDescription
        provenance['seriesuid'] = img.SeriesInstanceUID
        provenance['filesInSeries'] = [self.path]
        if hasattr(img, 'AcquisitionDateTime'):
            acqstring = img.AcquisitionDateTime.split('.')[0]
            dateformat = '%Y%m%d%H%M%S'
            provenance['acquired'] = datetime.strptime(acqstring,dateformat)
        else:
            dateformat = '%Y%m%d'
            acqdate = datetime.strptime(img.SeriesDate, dateformat)
            acqtime = datetime.fromtimestamp(float(img.SeriesTime)).time()
            provenance['acquired'] = datetime.combine(acqdate, acqtime) 
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
        
        
