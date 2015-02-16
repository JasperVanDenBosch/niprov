#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.externals import Externals
from niprov.logging import log


def record(command, new=None, parent=None, externals=Externals()):
    """Execute a command and log it as provenance for the newly created file.

    Args:
        command (list): Commands to be executed
        new (str): (optional) Override path to the new file, i.e. if it 
            cannot be parsed from the command.
        parent (str): (optional) Override path to the parent file, i.e. if it 
            cannot be parsed from the command.

    Returns:
        dict: New provenance
    """
    result = externals.run(command)
    transformation = command[0]
    code = ' '.join(command)
    for c in range(len(command)):
        if command[c] in ['-out']:
            _new = command[c+1]
        if command[c] in ['-in']:
            _parent = command[c+1]
    if parent:
        _parent = parent
    if new:
        _new = new
    return log(_new, transformation, _parent, code=code, logtext=result.output)
