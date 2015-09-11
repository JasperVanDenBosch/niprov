from niprov.config import Configuration
from niprov.commandline import Commandline
from niprov.jsonfile import JsonFile
from niprov.mongo import MongoRepository
from niprov.files import FileFactory
#import niprov.adding
#import niprov.approval

class Context(object):

    def __init__(self):
        self.config = Configuration()

    def reconfigure(self, newConfiguration):
        if newConfiguration is not None:
            self.config = newConfiguration

    def getListener(self):
        return Commandline(self.config)

    def getRepository(self):
        if self.config.database_type == 'file':
            return JsonFile()
        elif self.config.database_type == 'MongoDB':
            return MongoRepository()

    def getFileFactory(self):
        return FileFactory()

    def add(self, filepath, transient=False):
        """See :py:mod:`niprov.config`  """
        return niprov.adding.add(filepath, transient, context=self)

    def markForApproval(self, files):
        """See :py:mod:`niprov.approval`  """
        return niprov.approval.markForApproval(files, context=self)

    def markedForApproval(self):
        """See :py:mod:`niprov.approval`  """
        return niprov.approval.markedForApproval(context=self)

    def approve(self, filepath):
        """See :py:mod:`niprov.approval`  """
        return niprov.approval.approve(filepath, context=self)

    def selectApproved(self, files):
        """See :py:mod:`niprov.approval`  """
        return niprov.approval.selectApproved(files, context=self)

