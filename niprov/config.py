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
    or 'MongoDB'
    """

    database_url = '~/provenance.json'
    """str: URL of the database. If ``database-type`` is ``file``, this is the 
    path to the file."""

    dryrun = False
    """bool: Do not execute commands or make lasting changes to the 
    provenance database."""

    verbosity = 'info'
    """string: Level of information to report. One of 'debug','info','warning',
    'error'. Any level includes higher levels, i.e. 'info' will log messages of 
    that are deemed 'info', 'warning' or 'error'. """

    discover_file_extensions = ['.PAR','.dcm','.fif','.cnt']
    """list: Discover uses this to determine which files to include. 
    Not strictly extensions, can be any string that appears in the file name. 
    Use comma's to separate items."""

    attach = False
    """bool: Attach provenance to image files. For nifti files for instance,
    this means inserting a header extension with serialized provenance. See 
    'attach_format' to configure which data format is used."""

    attach_format = 'json'
    """string: Format in which to attach provenance to the file. One of 'json',
    or 'xml'.
    For example, if set to 'json' and the 'attach' option is True, this will 
    add a header extension to nifti files created with the relevant provenance 
    data in json format."""

    user = ''
    """string: Name of the user creating provenance. If not provided, will
    be determined based on OS information or as passed as an argument to the
    provenance operation. See also :py:mod:`niprov.users`"""

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
