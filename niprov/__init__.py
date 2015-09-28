from niprov.discovery import discover
from niprov.inspection import inspect
from niprov.reporting import report
from niprov.logging import log
from niprov.recording import record
from niprov.adding import add
from niprov.renaming import renameDicoms
from niprov.approval import (markForApproval, markedForApproval, approve, 
    selectApproved)
from niprov.context import Context
from niprov.config import Configuration

from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
#    settings = {}
#    settings['reload_all'] = True
#    settings['debug_all'] = True
#    settings['mako.directories'] = os.path.join(here, 'templates')
    config = Configurator(settings=settings)
    config.include('pyramid_mako')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()
