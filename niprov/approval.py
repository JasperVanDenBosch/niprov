#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.context import Context


def markForApproval(files, context=Context()):
    """Mark a list of files for approval by a human.

    Args:
        files (list): List of paths of files tracked by niprov to mark for
            approval.
    """
    repository = context.getRepository()
    for filepath in files:
        repository.updateApproval(filepath,'pending')

def markedForApproval(context=Context()):
    """List files marked for approval by a human.
    """
    repository = context.getRepository() 
    listener = context.getListener() 
    markedFiles = repository.byApproval('pending')
    listener.filesMarkedForApproval(markedFiles)
    return markedFiles

def approve(filepath, context=Context()):
    """Mark this file as approved.

    Args:
        filepath (str): Path to the tracked file that has been found valid.
    """
    repository = context.getRepository() 
    repository.updateApproval(filepath,'granted')

def selectApproved(files, context=Context()):
    """Return only files that have approval status 'granted'.

    Args:
        files (list): List of paths of files to check for approval status.
    """
    repository = context.getRepository() 
    selection = []
    for filepath in files:
        img = repository.byPath(filepath)
        if 'approval' in img.provenance:
            if img.provenance['approval'] == 'granted':
                selection.append(img.path)
    return selection
