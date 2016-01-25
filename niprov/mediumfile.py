from niprov.formatxml import XmlFormat
from niprov.formatjson import JsonFormat


class FileMedium(object):

    def __init__(self, dependencies):
        self.filesys = dependencies.getFilesystem()
        self.clock = dependencies.getClock()
        self.listener = dependencies.getListener()

    def export(self, formattedProvenance, form):
        fname = 'provenance_{0}.{1}'.format(self.clock.getNowString(),
            form.fileExtension)
        self.filesys.write(fname, formattedProvenance)
        self.listener.exportedToFile(fname)
        return fname
