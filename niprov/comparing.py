from niprov.diff import Diff


def compare(file1, file2, dependencies=None):
    """Compare the provenance of two files.

    This creates a niprov :class:`.Diff` object that can be further 
    interrogated or displayed for differences between the two files.

    Example:
        Chain calls with methods of Diff or print the Diff object::

            compare(file1, file2).assertEqual(ignore='path')
            print(compare(file1, file2))

    Args:
        file1 (:class:`.BaseFile`): One of two niprov BaseFile objects to compare.
        file2 (:class:`.BaseFile`): As file1

    Returns:
        niprov.diff.Diff: A niprov :class:`.Diff` object which reflects
            differences between the two files.
    """
    return Diff(file1, file2)
