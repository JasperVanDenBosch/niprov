#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.jsonfile import JsonFile
from niprov.commandline import Commandline


def markForApproval(files, repository=JsonFile()):
    """Mark a list of files for approval by a human.

    Args:
        files (list): List of paths of files tracked by niprov to mark for
            approval.
    """
    for filepath in files:
        repository.updateApproval(filepath,'pending')

def markedForApproval(repository=JsonFile(), listener=Commandline()):
    """List files marked for approval by a human.
    """
    markedFiles = repository.byApproval('pending')
    listener.filesMarkedForApproval(markedFiles)
    return markedFiles

def approve(filepath, repository=JsonFile()):
    """Mark this file as approved.

    Args:
        filepath (str): Path to the tracked file that has been found valid.
    """
    repository.updateApproval(filepath,'granted')
