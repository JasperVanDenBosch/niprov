import sys 
from cStringIO import StringIO 


class OutputCapture(object):
    """Context manager which records stdout writes.

    Used when recording python-based transformations.
    """

    def __enter__(self):
        self.oldstdout = sys.stdout 
        sys.stdout = self.stdout = StringIO()
        return self

    def __exit__(self, type, value, traceback):
        sys.stdout = self.oldstdout
        self.output = self.stdout.getvalue()
        self.stdout.close()
