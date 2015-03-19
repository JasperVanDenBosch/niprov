from niprov.filesystem import Filesystem
from jsonserializing import JsonSerializer
from niprov.files import FileFactory
import os


class JsonFile(object):
    """Stores provenance in a local text file encoded as json.
    """

    def __init__(self, filesys=Filesystem(), json=JsonSerializer(), 
            factory=FileFactory()):
        self.filesys = filesys
        self.json = json
        self.factory = factory
        self.datafile = os.path.expanduser(os.path.join('~','provenance.json'))

    def add(self, record):
        """Add the provenance for one file to storage.

        Args:
            record (dict): Provenance for one image file.
        """
        current = self.all()
        current.append(record)
        jsonstr = self.json.serializeList(current)
        with open(self.datafile, 'w') as fp:
            fp.write(jsonstr)

    def update(self, image):
        """Save changed provenance for this file..

        Args:
            image (:class:`.BaseFile`): Image file that has changed.
        """
        current = self.all()
        for r in range(len(current)):
            if current[r]['path'] == image.path:
                current[r] = image.provenance
        jsonstr = self.json.serializeList(current)
        with open(self.datafile, 'w') as fp:
            fp.write(jsonstr)

    def all(self):
        """Retrieve all known provenance from storage.

        Returns:
            list: List of provenance for known files.
        """
        try:
            jsonstr = self.filesys.read(self.datafile)
        except IOError:
            return []
        return self.json.deserializeList(jsonstr)

    def knowsByPath(self, path):
        """Whether the file at this path has provenance associated with it.

        Returns:
            bool: True if provenance is available for that path.
        """
        try:
            self.byPath(path)
        except IndexError:
            return False
        return True

    def knows(self, image):
        """Whether this file has provenance associated with it.

        Returns:
            bool: True if provenance is available for this image.
        """
        try:
            self.byPath(image.path)
        except IndexError:
            return False
        return True

    def knowsSeries(self, image):
        """Whether the series that this file is part of has provenance 
        associated with it.

        Args:
            image (:class:`.BaseFile`): File for which the series is sought.

        Returns:
            bool: True if provenance is available for this series.
        """
        try:
            self.getSeries(image)
        except IndexError:
            return False
        return True

    def byPath(self, path):
        """Get the provenance for a file at the given path. 

        In the case of a dicom series, this returns the provenance for the 
        series.

        Args:
            path (str): File system path to the image file.

        Returns:
            dict: Provenance for one image file.
        """
        for record in self.all():
            if record['path'] == path:
                return self.factory.fromProvenance(record)
            elif 'filesInSeries' in record and path in record['filesInSeries']:
                return self.factory.fromProvenance(record)
        else:
            raise IndexError('No file with that path known.')

    def bySubject(self, subject):
        """Get the provenance for all files of a given participant. 

        Args:
            subject (str): The name or other ID string.

        Returns:
            list: List of provenance for known files imaging this subject.
        """
        all = self.all()
        return [f for f in all if f['subject']==subject]

    def getSeries(self, image):
        """Get the object that carries provenance for the series that the image 
        passed is in. 

        Args:
            image (:class:`.DicomFile`): File that is part of a series.

        Returns:
            :class:`.DicomFile`: Image object that caries provenance for the series.
        """
        if image.getSeriesId() is None:
            raise IndexError('Image has no series id.')
        seriesId = image.getSeriesId()
        for record in self.all():
            if 'seriesuid' in record and record['seriesuid'] == seriesId:
                return self.factory.fromProvenance(record)
        else:
            raise IndexError('No provenance record for that series.')
       

