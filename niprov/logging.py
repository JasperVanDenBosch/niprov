#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.dependencies import Dependencies
from niprov.adding import add
import copy


def log(new, transformation, parents, code=None, logtext=None, transient=False,
        script=None, provenance=None, opts=None, dependencies=Dependencies()):
    """
    Register a transformation that creates a new image (or several).

    This will retrieve the primary parent's provenance. if no provenance is 
    availale for the primary parent, calls listener.unknownFile. Otherwise,
    some fields are copied from the primary parent, subject to availability. 
    For instance, if the parent has no 'subject' field, the new file's 
    provenance won't either.

    Args:
        new (str or list): Path(s) to the newly created file(s).
        transformation (str): Name of the operation that has been used.
        parents (str or list): Path(s) to the file(s) that were used as the 
            basis of the transformation. Assumes that the first file in the 
            list is the primary parent for which basic provenance is known.
        code (str, optional): Code that was used to generate the new file
        logtext (str, optional): Any information about the transformation that 
            was logged.
        script (str, optional): Path to the code file that contains the 
            transformation code.
        transient (bool, optional): Set this to True to indicate that the file 
            is only temporary and future checks should not expect it to be 
            physically present. Defaults to False, assuming that the file 
            remains.
        provenance (dict, optional): Add the key-value pairs in this dictionary 
            to the provenance record for the new files.
        opts (Configuration): General settings for niprov. 
            See :py:mod:`niprov.config`

    Raises:
      IOError: '[Errno 2] File not found' is raised if the new file does not
        exist on the filesystem and is not marked as transient.

    Returns:
        BaseFile: New provenance, if multiple files were created, this is 
            a list of images, otherwise, it is a single object.
    """
    repository = dependencies.getRepository()
    listener = dependencies.getListener()
    factory = dependencies.getFileFactory()
    filesys = dependencies.getFilesystem()
    opts = dependencies.reconfigureOrGetConfiguration(opts)
    location = dependencies.getLocationFactory()

    if isinstance(new, basestring):
        new = [new]
    if isinstance(parents, basestring):
        parents = [parents]
    if provenance is None:
        provenance = {}

    #gather provenance common to all new files
    commonProvenance = provenance
    commonProvenance['parents'] = [location.completeString(p) for p in parents]
    commonProvenance['transformation'] = transformation
    commonProvenance['script'] = script
    if code:
        commonProvenance['code'] = code
    if logtext:
        commonProvenance['logtext'] = logtext
    if repository.knowsByLocation(commonProvenance['parents'][0]):
        parentProvenance = repository.byLocation(
            commonProvenance['parents'][0]).provenance
        for field in ['acquired','subject','protocol']:
            if field in parentProvenance:
                commonProvenance[field] = parentProvenance[field]
    else:
        listener.unknownFile(parents[0])
        return

    #do things specific to each new file
    newImages = []
    for newfile in new:
        singleProvenance = copy.deepcopy(commonProvenance)
        image = add(newfile, transient=transient, provenance=singleProvenance, 
            dependencies=dependencies)
        newImages.append(image)

    #only return one image if only one file was created
    if len(new) == 1:
        return image

    return newImages



    
