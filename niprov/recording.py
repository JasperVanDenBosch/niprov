#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.externals import Externals
from niprov.logging import log


def record(command, externals=Externals()):
    """Execute a command and log it as provenance for the newly created file.

    Args:
        command (list): Commands to be executed

    Returns:
        dict: New provenance
    """
    result = externals.run(command)
    transformation = command[0]
    code = ' '.join(command)
    for c in range(len(command)):
        if command[c] in ['-out']:
            new = command[c+1]
        if command[c] in ['-in']:
            ancestor = command[c+1]
    return log(transformation, ancestor, new, code=code, logtext=result.output)
