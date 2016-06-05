#!/usr/bin/python
# -*- coding: UTF-8 -*-
import webbrowser


class ViewerMedium(object):
    """Uses the system picture viewer to display an picture file.
    """

    def __init__(self, dependencies):
        pass

    def export(self, formattedProvenance, form=None):
        if formattedProvenance is None:
            return
        webbrowser.open(formattedProvenance)

