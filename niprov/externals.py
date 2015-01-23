#!/usr/bin/python
# -*- coding: UTF-8 -*-
import subprocess

class Externals(object):
    """Utility that wraps the python subprocess module to start other applications
    """

    def run(self, command):
        """Start a subprocess with the command provided.

        Args:
            command (list): A list of command elements.
        """
        output = subprocess.check_output(command)
        return Result(True, output)


class Result(object):

    def __init__(self, succesful, output):
        self.succesful = succesful
        self.output = output
