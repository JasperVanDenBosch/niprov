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
        subprocess.check_call(command)
