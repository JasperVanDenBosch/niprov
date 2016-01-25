

class FileMedium(object):

    def __init__(self, dependencies):
        self.filesys = dependencies.getFilesystem()
        self.clock = dependencies.getClock()
        self.listener = dependencies.getListener()

    def export(self, formattedProvenance):
        fname = 'provenance_{0}.txt'.format(self.clock.getNowString())
        self.filesys.write(fname, formattedProvenance)
        self.listener.exportedToFile(fname)
        return fname
