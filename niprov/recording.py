#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.externals import Externals
from niprov.logging import log
from niprov.commandline import Commandline


def record(command, new=[], parents=[], transient=False, args=[], kwargs={},
    externals=Externals(), listener=Commandline()):
    """Execute a command and log it as provenance for the newly created file.

    Args:
        command (list or str or callable): Command to be executed. Either a 
            string of executable system code, a list of components thereof, or 
            a python function object. 
        new (list or str, optional): Override path to the new file(s), i.e. if 
            they cannot be parsed from the command.
        parents (list or str, optional): Override paths to parent file(s), i.e. 
            if they cannot be parsed from the command.
        transient (bool, optional): Set this to True to indicate that the file 
            is only temporary and future checks should not expect it to be 
            physically present. Defaults to False, assuming that the file 
            remains.
        args (list, optional): Positional arguments to be passed to command.
        kwargs (dict, optional): Keyword arguments to be passed to command.

    Returns:
        dict: New provenance
    """
    if isinstance(new, basestring):
        new = [new]
    if isinstance(parents, basestring):
        parents = [parents]
    if isinstance(command, basestring):
        command = command.split()
    provenance = {}
    if isinstance(command, (list, tuple)):
        transformation = command[0]
        code = ' '.join(command)
        script = None
        parsingNew = len(new) == 0
        parsingParents = len(parents) == 0
        for c in range(len(command)):
            if command[c] in ['-out'] and parsingNew:
                new.append(command[c+1])
            if command[c] in ['-in'] and parsingParents:
                parents.append(command[c+1])
    else:
        transformation = command.func_name
        script = command.func_code.co_filename
        code = None
        provenance['args'] = args
        provenance['kwargs'] = kwargs

    listener.interpretedRecording(new, transformation, parents)

    if isinstance(command, (list, tuple)):
        result = externals.run(command)
        output = result.output
    else:
        command(*args, **kwargs)
        output = None

    return log(new, transformation, parents, code=code, transient=transient,
        logtext=output, script=script, provenance=provenance)
