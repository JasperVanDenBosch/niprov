#!/usr/bin/python
# -*- coding: UTF-8 -*-
import webbrowser


class ViewerMedium(object):
    """Uses the system picture viewer to display an picture file.
    """

    def export(self, formattedProvenance, form):
        webbrowser.open(formattedProvenance)

