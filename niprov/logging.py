#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.jsonfile import JsonFile
from niprov.filesystem import Filesystem
import errno


def log(new, transformation, parents, code=None, logtext=None, transient=False,
        repository=JsonFile(), filesys=Filesystem()):
    """
    Register a transformation that creates a new image.

    Args:
        new (str): Path to the newly created file.
        transformation (str): Name of the operation that has been used.
        parents (list): Paths to the files that were used as the basis of the 
            transformation. Assumes that the first file in the list is the 
            primary parent for which basic provenance is known.
        code (str, optional): Code that was used to generate the new file
        logtext (str, optional): Any information about the transformation that 
            was logged.
        transient (bool, optional): Set this to True to indicate that the file 
            is only temporary and future checks should not expect it to be 
            physically present. Defaults to False, assuming that the file 
            remains.

    Raises:
      IOError: '[Errno 2] File not found' is raised if the new file does not
        exist on the filesystem and is not marked as transient.

    Returns:
        dict: New provenance
    """
    if not transient and not filesys.fileExists(new):
        raise IOError(errno.ENOENT, 'File not found', new)
    provenance = {}
    provenance['parents'] = parents
    provenance['path'] = new
    provenance['transformation'] = transformation
    provenance['transient'] = transient
    if code:
        provenance['code'] = code
    if logtext:
        provenance['logtext'] = logtext
    if repository.knowsByPath(parents[0]):
        parentProvenance = repository.byPath(parents[0])
        provenance['acquired'] = parentProvenance['acquired']
        provenance['subject'] = parentProvenance['subject']
        provenance['protocol'] = parentProvenance['protocol']
    repository.add(provenance)
    return provenance



    
