

class Diff(object):

    defaultIgnore = ['_id']

    def __init__(self, file1, file2):
        self.file1 = file1
        self.file2 = file2

    def _checkDiff(self, ignore=None):
        assert isinstance(ignore, list) or ignore is None
        if ignore is None:
            ignore = []
        ignore += self.defaultIgnore
        diffDict = {}
        prov1 = self.file1.getProvenance()
        prov2 = self.file2.getProvenance()
        for k in set(prov1.keys()).difference(prov2.keys()):
            if k not in ignore:
                diffDict[k] = 'missingIn2'
        for k in set(prov2.keys()).difference(prov1.keys()):
            if k not in ignore:
                diffDict[k] = 'missingIn1'
        for k in set(prov1.keys()).intersection(prov2.keys()):
            if k not in ignore:
                if prov1[k] != prov2[k]:
                    diffDict[k] = 'value'
        return diffDict

    def areEqual(self, ignore=None):
        return len(self._checkDiff(ignore)) == 0

    def assertEqual(self):
        if not self.areEqual():
            raise AssertionError()

    def assertEqualProtocol(self):
        pass
