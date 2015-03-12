import os, shutil, glob
from niprov.commandline import Commandline


def renameDicoms(dicomdir, listener=Commandline()):
    """ Add the .dcm extension to any non-hidden files without extension.

        Args:
            dicomdir (str): Directory in which to rename files.
    """
    for f in glob.glob(os.path.join(dicomdir, '*')):
        if '.' not in os.path.basename(f):
            listener.renamedDicom(f)
            shutil.move(f, f+'.dcm')
