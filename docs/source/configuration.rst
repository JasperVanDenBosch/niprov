Configuration
=============

Niprov can be configured through a text file with configuration directives.
This file is located at ~/niprov.cfg.
Alternatively, the settings can be changed in code:
::

    from niprov.config import Configuration
    conf = Configuration
    conf.verbose = True
    niprov.log(x,y,z, opts=conf)




See :class:`niprov.config.Configuration` for details on the individual settings.




