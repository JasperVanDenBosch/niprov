

class Diff(object):

    def __init__(self, file1, file2):
        self.diffDict = {}
        self.ignore = ['_id']
        prov1 = file1.getProvenance()
        prov2 = file2.getProvenance()
        for k in set(prov1.keys()).difference(prov2.keys()):
            if k not in self.ignore:
                self.diffDict[k] = 'missingIn2'
        for k in set(prov2.keys()).difference(prov1.keys()):
            if k not in self.ignore:
                self.diffDict[k] = 'missingIn1'
        for k in set(prov1.keys()).intersection(prov2.keys()):
            if k not in self.ignore:
                if prov1[k] != prov2[k]:
                    self.diffDict[k] = 'value'

    def areEqual(self):
        return len(self.diffDict) == 0

    def assertEqual(self):
        if not self.areEqual():
            raise AssertionError()

    def assertEqualProtocol(self):
        pass
