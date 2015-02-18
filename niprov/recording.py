#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.externals import Externals
from niprov.logging import log
from niprov.commandline import Commandline


def record(command, new=None, parents=None, transient=False, 
    externals=Externals(), listener=Commandline()):
    """Execute a command and log it as provenance for the newly created file.

    Args:
        command (list or str): Commands to be executed
        new (str): (optional) Override path to the new file, i.e. if it 
            cannot be parsed from the command.
        parents (list): (optional) Override paths to parent files, i.e. if they 
            cannot be parsed from the command.
        transient (bool, optional): Set this to True to indicate that the file 
            is only temporary and future checks should not expect it to be 
            physically present. Defaults to False, assuming that the file 
            remains.

    Returns:
        dict: New provenance
    """
    if isinstance(command, basestring):
        command = command.split()
    transformation = command[0]
    code = ' '.join(command)
    for c in range(len(command)):
        if command[c] in ['-out']:
            _new = command[c+1]
        if command[c] in ['-in']:
            _parents = [command[c+1]]
    if parents is not None:
        _parents = parents
    if new:
        _new = new
    listener.interpretedRecording(_new, transformation, _parents)
    result = externals.run(command)
    return log(_new, transformation, _parents, code=code, transient=transient,
        logtext=result.output)
