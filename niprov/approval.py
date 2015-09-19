#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.dependencies import Dependencies


def markForApproval(files, dependencies=Dependencies()):
    """Mark a list of files for approval by a human.

    Args:
        files (list): List of paths of files tracked by niprov to mark for
            approval.
    """
    repository = dependencies.getRepository()
    for filepath in files:
        repository.updateApproval(filepath,'pending')

def markedForApproval(dependencies=Dependencies()):
    """List files marked for approval by a human.
    """
    repository = dependencies.getRepository() 
    listener = dependencies.getListener() 
    markedFiles = repository.byApproval('pending')
    listener.filesMarkedForApproval(markedFiles)
    return markedFiles

def approve(filepath, dependencies=Dependencies()):
    """Mark this file as approved.

    Args:
        filepath (str): Path to the tracked file that has been found valid.
    """
    repository = dependencies.getRepository() 
    repository.updateApproval(filepath,'granted')

def selectApproved(files, dependencies=Dependencies()):
    """Return only files that have approval status 'granted'.

    Args:
        files (list): List of paths of files to check for approval status.
    """
    repository = dependencies.getRepository() 
    location = dependencies.getLocationFactory()
    selection = []
    for filepath in files:
        locationString = location.completeString(filepath)
        img = repository.byLocation(locationString)
        if 'approval' in img.provenance:
            if img.provenance['approval'] == 'granted':
                selection.append(img.path)
    return selection
