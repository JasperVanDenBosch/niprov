from niprov.dependencies import Dependencies
from niprov.config import Configuration
import niprov.adding
import niprov.approval
import niprov.discovery
import niprov.inspection

class Context(object):

    def __init__(self):
        self.config = Configuration()
        self.deps = Dependencies(self.config)

    def add(self, filepath, transient=False):
        """See :py:mod:`niprov.config`  """
        return niprov.adding.add(filepath, transient, dependencies=self.deps)

    def discover(self, root):
        """See :py:mod:`niprov.discovery`  """
        return niprov.discovery.discover(root, dependencies=self.deps)

    def inspect(self, fpath):
        """See :py:mod:`niprov.inspection`  """
        return niprov.inspection.inspect(fpath, dependencies=self.deps)

    def markForApproval(self, files):
        """See :py:mod:`niprov.approval`  """
        return niprov.approval.markForApproval(files, dependencies=self.deps)

    def markedForApproval(self):
        """See :py:mod:`niprov.approval`  """
        return niprov.approval.markedForApproval(dependencies=self.deps)

    def approve(self, filepath):
        """See :py:mod:`niprov.approval`  """
        return niprov.approval.approve(filepath, dependencies=self.deps)

    def selectApproved(self, files):
        """See :py:mod:`niprov.approval`  """
        return niprov.approval.selectApproved(files, dependencies=self.deps)

