#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.commandline import Commandline
from niprov.dependencies import Dependencies


def inspect(fpath, listener=Commandline(), libs=Dependencies()):
    if libs.hasDependency('nibabel'):
        libs.nibabel.load(fpath)

    
