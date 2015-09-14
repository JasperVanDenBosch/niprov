import os, shutil, glob
from niprov.dependencies import Dependencies


def renameDicoms(dicomdir, dependencies=Dependencies()):
    """ Add the .dcm extension to any non-hidden files without extension.

        Args:
            dicomdir (str): Directory in which to rename files.
    """
    listener = dependencies.getListener()

    for f in glob.glob(os.path.join(dicomdir, '*')):
        if '.' not in os.path.basename(f):
            listener.renamedDicom(f)
            shutil.move(f, f+'.dcm')
