#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.dependencies import Dependencies


def markForApproval(files, reset=False, dependencies=Dependencies()):
    """Mark a list of files for approval by a human.

    Args:
        files (list): List of paths of files tracked by niprov to mark for
            approval.
        reset (bool): Also mark files that have already been approved. False 
            by default.
    """
    repository = dependencies.getRepository()
    location = dependencies.getLocationFactory()
    for filepath in files:
        loc = location.completeString(filepath)
        if not reset:
            image = repository.byLocation(loc)
            if image is None:
                raise ValueError('Unknown file: '+filepath)
            if image.provenance.get('approval') == 'granted':
                continue
        repository.updateApproval(loc,'pending')

def markedForApproval(dependencies=Dependencies()):
    """List files marked for approval by a human.
    """
    query = dependencies.getQuery() 
    listener = dependencies.getListener() 
    markedFiles = query.byApproval('pending')
    listener.filesMarkedForApproval(markedFiles)
    return markedFiles

def approve(filepath, dependencies=Dependencies()):
    """Mark this file as approved.

    Args:
        filepath (str): Path to the tracked file that has been found valid.
    """
    loc = dependencies.getLocationFactory().completeString(filepath)
    repository = dependencies.getRepository()
    repository.updateApproval(loc, 'granted')

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
        if img.provenance.get('approval') == 'granted':
            selection.append(img.path)
    return selection
