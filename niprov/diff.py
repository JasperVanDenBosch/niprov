from os.path import basename

class Diff(object):
    """Difference between two files.

    This represents differences in provenance between two files.

    See :py:mod:`niprov.comparing`

    Args:
        file1 (:class:`.BaseFile`): One of two niprov BaseFile objects to 
            compare.
        file2 (:class:`.BaseFile`): As file1
    """

    NCHARSCOL = 20              # width of columns
    defaultIgnore = ['_id']     # these fields are always ignored

    def __init__(self, file1, file2):
        self.file1 = file1
        self.file2 = file2

    def getDifferences(self, ignore=None, select=None):
        """Get dictionary with fields that differ and how they differ.

        Args:
            ignore (list): Optional. List of fields not to evaluate when 
                determining differences.
            select (list): Optional. List of fields that should be specifically
                evaluated. All other fields will be ignored.

        Returns:
            dict: A dictionary with provenance fields as keys and strings
                indicating how they differ.
        """
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

    def getSame(self):
        """Get dictionary with fields that have equal values.

        Returns:
            dict: A dictionary with provenance fields as keys the string
                  'same' as value.
        """
        prov1 = self.file1.getProvenance()
        prov2 = self.file2.getProvenance()
        sameDict = {}
        for k in set(prov1.keys()).intersection(prov2.keys()):
            if prov1[k] == prov2[k]:
                sameDict[k] = 'same'
        return sameDict

    def getDifferenceString(self, ignore=None, select=None):
        """Get table of differences as string.

        Args:
            ignore (list): Optional. List of fields not to evaluate when 
                determining differences.
            select (list): Optional. List of fields that should be specifically
                evaluated. All other fields will be ignored.

        Returns:
            str: A three-columns table listing provenance fields and their
                respective values for the two files.
        """
        differences = self.getDifferences(ignore, select)
        return self._tableStringFromDiffDict(differences)

    def getSameString(self):
        """Get table of values that are the same for the compared files.

        Returns:
            str: A three-columns table listing provenance fields and their
                respective values for the two files.
        """
        same = self.getSame()
        return self._tableStringFromDiffDict(same)

    def _tableStringFromDiffDict(self, diffDict):
        if not diffDict:
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
        for field, status in diffDict.items():
            val1 = prov1.get(field, 'n/a')
            val2 = prov2.get(field, 'n/a')
            diffStr += row(field, str(val1), str(val2))
        return diffStr

    def areEqual(self, ignore=None, select=None):
        """Whether there are any differences between the files.

        Args:
            ignore (list): Optional. List of fields not to evaluate when 
                determining differences.
            select (list): Optional. List of fields that should be specifically
                evaluated. All other fields will be ignored.

        Returns:
            bool: True if no differences, False otherwise.
        """
        differences = self.getDifferences(ignore, select)
        return len(differences) == 0

    def areEqualProtocol(self):
        """Whether there are any differences for protocol fields.

        Each :class:`.BaseFile` subtype has a getProtocolFields() method
        that is used here to selectively see if any of these are different.

        Returns:
            bool: True if no differences, False otherwise.
        """
        protocol = self.file1.getProtocolFields()
        differences = self.getDifferences(select=protocol)
        return len(differences) == 0

    def assertEqual(self, ignore=None, select=None):
        """Raises exception if there are differences.

        Args:
            ignore (list): Optional. List of fields not to evaluate when 
                determining differences.
            select (list): Optional. List of fields that should be specifically
                evaluated. All other fields will be ignored.

        Raises:
            AssertionError: Message with differences in a table.
        """
        differences = self.getDifferenceString(ignore, select)
        if differences:
            raise AssertionError(differences)

    def assertEqualProtocol(self):
        """Raises exception if there are differences in protocol fields.

        Each :class:`.BaseFile` subtype has a getProtocolFields() method
        that is used here to selectively see if any of these are different.

        Raises:
            AssertionError: Message with protocol differences in a table.
        """
        protocol = self.file1.getProtocolFields()
        differences = self.getDifferenceString(select=protocol)
        if differences:
            raise AssertionError(differences)

    def __str__(self):
        return self.getDifferenceString()
