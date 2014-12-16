#!/usr/bin/python
# -*- coding: UTF-8 -*-
from niprov.filesystem import Filesystem

def discover(root, filesys=Filesystem(), listener=None):
    files = filesys.glob(root)
    for filepath in files:
        listener.fileFound(filepath)
    
