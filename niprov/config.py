import os, ConfigParser


class Configuration(object):
    """General settings for niprov.

    Individual settings are documented as follows;

    **setting** *= default_value*
        *type* - Explanation.

    The settings can be changed in the configuration file, or in code.

    All settings:
    """
    database_type = 'file'
    """str: Type of backend in which to store provenance. Currently only 'file'
    """

    database_url = '~/provenance.json'
    """str: URL of the database. If ``database-type`` is ``file``, this is the 
    path to the file."""

    dryrun = False
    """bool: Do not execute commands or make lasting changes to the 
    provenance database."""

    verbose = False
    """bool: Output extra information."""

    discover_file_extensions = ['.PAR','.dcm','.fif','.cnt']
    """list: Discover uses this to determine which files to include. 
    Not strictly extensions, can be any string that appears in the file name. 
    Use comma's to separate items."""

    def __init__(self, configFilePath='~/niprov.cfg'):
        configFilePath = os.path.expanduser(configFilePath)
        if os.path.isfile(configFilePath):
            keys = [k for k in dir(self) if k[0] != '_']
            defaults = {k:getattr(self, k) for k in keys}
            types = {k:type(defaults[k]) for k in keys}
            parser = ConfigParser.SafeConfigParser()
            parser.read(configFilePath)
            for key in keys:
                if not parser.has_option('main', key):
                    val = defaults[key]
                elif types[key] is str:
                    val = parser.get('main', key)
                elif types[key] is bool:
                    val = parser.getboolean('main', key)
                elif types[key] is list:
                    items = parser.get('main', key).split(',')
                    val = [i.strip() for i in items if i is not '']
                setattr(self, key, val)
