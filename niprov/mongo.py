import pymongo
from niprov.dependencies import Dependencies


class MongoRepository(object):

    def __init__(self, dependencies=Dependencies()):
        self.config = dependencies.getConfiguration()
        self.factory = dependencies.getFileFactory()
        client = pymongo.MongoClient(self.config.database_url)
        self.db = client.get_default_database()

    def byPath(self, path):
        """Get the provenance for a file at the given path. 

        In the case of a dicom series, this returns the provenance for the 
        series.

        Args:
            path (str): File system path to the image file.

        Returns:
            dict: Provenance for one image file.
        """
        record = self.db.provenance.find_one({'path':path})
        return self.factory.fromProvenance(record)

    def knowsByPath(self, path):
        """Whether the file at this path has provenance associated with it.

        Returns:
            bool: True if provenance is available for that path.
        """
        return self.db.provenance.find_one({'path':path}) is not None

    def knows(self, image):
        """Whether this file has provenance associated with it.

        Returns:
            bool: True if provenance is available for this image.
        """
        return self.knowsByPath(image.path)

    def getSeries(self, image):
        """Get the object that carries provenance for the series that the image 
        passed is in. 

        Args:
            image (:class:`.DicomFile`): File that is part of a series.

        Returns:
            :class:`.DicomFile`: Image object that caries provenance for the series.
        """
        seriesId = image.getSeriesId()
        record = self.db.provenance.find_one({'seriesuid':seriesId})
        return self.factory.fromProvenance(record)

    def knowsSeries(self, image):
        """Whether this file is part of a series for which provenance 
        is available.

        Args:
            image (:class:`.BaseFile`): File for which the series is sought.

        Returns:
            bool: True if provenance is available for this series.
        """
        seriesUid = image.getSeriesId()
        if seriesUid is None:
            return False

