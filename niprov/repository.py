

class Repository(object):

    def byLocation(self, locationString):                     # pragma: no cover
        """Get the provenance for a file at the given location. 

        In the case of a dicom series, this returns the provenance for the 
        series.

        Args:
            locationString (str): Location of the image file.

        Returns:
            dict: Provenance for one image file.
        """

    def knowsByLocation(self, locationString):                # pragma: no cover
        """Whether the file at this location has provenance associated with it.

        Returns:
            bool: True if provenance is available for that path.
        """

    def knows(self, image):                                   # pragma: no cover
        """Whether this file has provenance associated with it.

        Returns:
            bool: True if provenance is available for this image.
        """

    def getSeries(self, image):                               # pragma: no cover
        """Get the object that carries provenance for the series that the image 
        passed is in. 

        Args:
            image (:class:`.DicomFile`): File that is part of a series.

        Returns:
            :class:`.DicomFile`: Image object that caries provenance for the series.
        """

    def knowsSeries(self, image):                             # pragma: no cover
        """Whether this file is part of a series for which provenance 
        is available.

        Args:
            image (:class:`.BaseFile`): File for which the series is sought.

        Returns:
            bool: True if provenance is available for this series.
        """

    def add(self, image):                                     # pragma: no cover
        """Add the provenance for one file to storage.

        Args:
            image (:class:`.BaseFile`): Image file to store.
        """

    def update(self, image):                                  # pragma: no cover
        """Save changed provenance for this file..

        Args:
            image (:class:`.BaseFile`): Image file that has changed.
        """

    def all(self):                                            # pragma: no cover
        """Retrieve all known provenance from storage.

        Returns:
            list: List of provenance for known files.
        """

    def bySubject(self, subject):                             # pragma: no cover
        """Get the provenance for all files of a given participant. 

        Args:
            subject (str): The name or other ID string.

        Returns:
            list: List of provenance for known files imaging this subject.
        """

    def byApproval(self, approvalStatus):                     # pragma: no cover
        """"""

    def updateApproval(self, locationString, approvalStatus): # pragma: no cover
        """"""

    def latest(self, n=20):                                   # pragma: no cover
        """Get the images that have been registered last. 

        Args:
            n (int): The number of files to retrieve. Defaults to 20.

        Returns:
            list: List of BaseFile objects.
        """

    def byId(self, uid):                                      # pragma: no cover
        """Get the provenance for a file with the given id. 

        Args:
            uid (str): Unique id for the file.

        Returns:
            BaseFile: File with the given id.
        """

    def byLocations(self, listOfLocations):                   # pragma: no cover
        """Get any files that match one of these locations 

        In the case of a dicom series, this returns the provenance for the 
        series.

        Args:
            listOfLocations (list): List of image locations.

        Returns:
            list: List with BaseFile objects
        """
