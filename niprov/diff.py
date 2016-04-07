

class Diff(object):

    defaultIgnore = ['_id']

    def __init__(self, file1, file2):
        self.file1 = file1
        self.file2 = file2

    def _checkDiff(self, ignore=None, select=None):
        assert isinstance(ignore, list) or ignore is None
        if ignore is None:
            ignore = []
        ignore += self.defaultIgnore
        prov1 = self.file1.getProvenance()
        prov2 = self.file2.getProvenance()
        if select:
            allkeys = set(prov1.keys()+prov2.keys())
            ignore = [k for k in allkeys if k not in select]
        diffDict = {}
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

    def areEqual(self, ignore=None, select=None):
        return len(self._checkDiff(ignore, select)) == 0

    def areEqualProtocol(self):
        protocol = self.file1.getProtocolFields()
        return self.areEqual(select=protocol)

    def assertEqual(self):
        if not self.areEqual():
            raise AssertionError()

    def assertEqualProtocol(self):
        pass
