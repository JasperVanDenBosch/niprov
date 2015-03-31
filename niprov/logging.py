#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.jsonfile import JsonFile
from niprov.filesystem import Filesystem
from niprov.commandline import Commandline
import errno
import copy


def log(new, transformation, parents, code=None, logtext=None, transient=False,
        script=None, provenance=None, repository=JsonFile(), filesys=Filesystem(),
        listener=Commandline()):
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

    Raises:
      IOError: '[Errno 2] File not found' is raised if the new file does not
        exist on the filesystem and is not marked as transient.

    Returns:
        dict or list: New provenance, if multiple files were created, this is 
            a list of dicts, otherwise, it is a single dict.
    """
    if isinstance(new, basestring):
        new = [new]
    if isinstance(parents, basestring):
        parents = [parents]
    if provenance is None:
        provenance = {}

    #gather provenance common to all new files
    commonProvenance = provenance
    commonProvenance['parents'] = parents
    commonProvenance['transformation'] = transformation
    commonProvenance['script'] = script
    commonProvenance['transient'] = transient
    if code:
        commonProvenance['code'] = code
    if logtext:
        commonProvenance['logtext'] = logtext
    if repository.knowsByPath(parents[0]):
        parentProvenance = repository.byPath(parents[0]).provenance
        for field in ['acquired','subject','protocol']:
            if field in parentProvenance:
                commonProvenance[field] = parentProvenance[field]
    else:
        listener.unknownFile(parents[0])
        return

    #do things specific to each new file
    provenance = []
    for newfile in new:
        singleProvenance = copy.deepcopy(commonProvenance)
        singleProvenance['path'] = newfile
        if not transient and not filesys.fileExists(newfile):
            raise IOError(errno.ENOENT, 'File not found', newfile)
        repository.add(singleProvenance)
        provenance.append(singleProvenance)

    #only return one dict if only one new file was created
    if len(new) == 1:
        return singleProvenance

    return provenance



    
