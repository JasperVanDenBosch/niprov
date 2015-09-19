import os
from niprov.dependencies import Dependencies
from basefile import BaseFile
from dcm import DicomFile
from parrec import ParrecFile
from fif import FifFile
from niprov.cnt import NeuroscanFile


class FileFactory(object):
    """Creates customized File objects.

    Based on libraries (python packages) installed and the filename, will
    return an object that derives from niprov.basefile.BaseFile.
    """

    formats = {'.par':('nibabel', ParrecFile),
               '.dcm':('dicom', DicomFile),
               '.cnt':(None, NeuroscanFile),
               '.fif':('mne',FifFile)}

    def __init__(self, dependencies=Dependencies()):
        self.libs = dependencies.getLibraries()
        self.listener = dependencies.getListener()
        self.dependencies = dependencies
    
    def locatedAt(self, location, provenance=None):
        """Return an object to represent the image file at the given location.

        If no specific class is available to handle a file with the filename 
        provided, will default to a BaseFile. Similarly, if missing the 
        dependency to deal with the format, will fall back to a regular 
        BaseFile.

        Args:
            location: Path to the file to represent.

        Returns:
            :class:`.BaseFile`: An object that derives from BaseFile
        """
        extension = os.path.splitext(location)[1].lower()
        if extension not in self.formats:
            return BaseFile(location, provenance=provenance, 
                dependencies=self.dependencies)
        elif not self.libs.hasDependency(self.formats[extension][0]):
            self.listener.missingDependencyForImage(
                self.formats[extension][0], location)
            return BaseFile(location, 
                dependencies=self.dependencies)
        return self.formats[extension][1](location, provenance=provenance, 
                dependencies=self.dependencies)

    def fromProvenance(self, provenance):
        return self.locatedAt(provenance['location'], provenance)




