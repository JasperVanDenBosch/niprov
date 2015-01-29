import os
from niprov.dependencies import Dependencies
from niprov.commandline import Commandline
from basefile import BaseFile
from dcm import DicomFile
from parrec import ParrecFile
from fif import FifFile


class FileFactory(object):
    """Creates customized File objects.

    Based on dependencies (python packages) installed and the filename, will
    return an object that derives from niprov.basefile.BaseFile.
    """

    formats = {'.par':('nibabel', ParrecFile),
               '.dcm':('dicom', DicomFile),
               '.fif':('mne',FifFile)}

    def __init__(self, libs=Dependencies(), listener=Commandline()):
        self.libs = libs
        self.listener = listener
    
    def locatedAt(self, path):
        """Return an object to represent the image file at the given path.

        If no specific class is available to handle a file with the filename 
        provided, will default to a BaseFile. Similarly, if missing the 
        dependency to deal with the format, will fall back to a regular 
        BaseFile.

        Args:
            path: Path to the file to represent.

        Returns:
            BaseFile: An object that derives from BaseFile
        """
        extension = os.path.splitext(path)[1].lower()
        if extension not in self.formats:
            return BaseFile(path)
        elif not self.libs.hasDependency(self.formats[extension][0]):
            self.listener.missingDependencyForImage(
                self.formats[extension][0], path)
            return BaseFile(path)
        return self.formats[extension][1](path)




