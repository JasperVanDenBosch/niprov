from os.path import basename

class Diff(object):

    NCHARSCOL = 20
    defaultIgnore = ['_id']

    def __init__(self, file1, file2):
        self.file1 = file1
        self.file2 = file2

    def getDifferences(self, ignore=None, select=None):
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

    def getDifferenceString(self, ignore=None, select=None):

        differences = self.getDifferences(ignore, select)
        if not differences:
            return ''
        name1 = basename(str(self.file1.location))
        name2 = basename(str(self.file2.location))
        prov1 = self.file1.getProvenance()
        prov2 = self.file2.getProvenance()
        def row(*vals):
            cells = [c[:self.NCHARSCOL] for c in vals]
            cells = [c.ljust(self.NCHARSCOL) for c in cells]
            return ' '.join(cells)+'\n'
        diffStr = 'Differences:\n'
        diffStr += row('', name1, name2)
        for field, status in differences.items():
            val1 = prov1.get(field, 'n/a')
            val2 = prov2.get(field, 'n/a')
            diffStr += row(field, str(val1), str(val2))
        return diffStr

    def areEqual(self, ignore=None, select=None):
        differences = self.getDifferences(ignore, select)
        return len(differences) == 0

    def areEqualProtocol(self):
        protocol = self.file1.getProtocolFields()
        differences = self.getDifferences(select=protocol)
        return len(differences) == 0

    def assertEqual(self, ignore=None, select=None):
        differences = self.getDifferenceString(ignore, select)
        if differences:
            raise AssertionError(differences)

    def assertEqualProtocol(self):
        protocol = self.file1.getProtocolFields()
        differences = self.getDifferenceString(select=protocol)
        if differences:
            raise AssertionError(differences)

    def __str__(self):
        return self.getDifferenceString()
