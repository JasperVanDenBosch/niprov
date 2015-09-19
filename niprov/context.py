from niprov.dependencies import Dependencies
from niprov.config import Configuration
import niprov


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

    def inspect(self, location):
        """See :py:mod:`niprov.inspection`  """
        return niprov.inspection.inspect(location, dependencies=self.deps)

    def log(self, *args, **kwargs):
        """See :py:mod:`niprov.logging`  """
        return niprov.logging.log(*args, dependencies=self.deps, **kwargs)

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

    def renameDicoms(self, dicomdir):
        """See :py:mod:`niprov.renaming`  """
        return niprov.renaming.renameDicoms(dicomdir, dependencies=self.deps)

    def record(self, *args, **kwargs):
        """See :py:mod:`niprov.recording`  """
        return niprov.recording.record(*args, dependencies=self.deps, **kwargs)

    def report(self, *args, **kwargs):
        """See :py:mod:`niprov.reporting`  """
        return niprov.reporting.report(*args, dependencies=self.deps, **kwargs)
