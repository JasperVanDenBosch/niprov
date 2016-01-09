

class FileMedium(object):

    def __init__(self, dependencies):
        self.filesys = dependencies.getFilesystem()
        self.clock = dependencies.getClock()

    def export(self, formattedProvenance):
        fname = 'provenance_{0}.txt'.format(self.clock.getNowString())
        self.filesys.write(fname, formattedProvenance)
        return fname
