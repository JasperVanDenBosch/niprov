from pyramid.config import Configurator
import waitress, os
from niprov.dependencies import Dependencies


def serve():
    wsgiapp = main(None)
    waitress.serve(wsgiapp, host='0.0.0.0', port=6543)

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
#    settings = {}
#    settings['reload_all'] = True
#    settings['debug_all'] = True
#    settings['mako.directories'] = os.path.join(here, 'templates')
    config = Configurator(settings=settings)
    config.include('pyramid_mako')
    config.add_static_view('static', 'static', cache_max_age=10)
    config.add_static_view('snapshots', 
        os.path.expanduser('~/.niprov-snapshots'), cache_max_age=10)
    config.add_route('home', '/')
    config.add_route('latest', '/latest')
    config.add_route('stats', '/stats')
    config.add_route('short', '/id/{id}')
    config.add_route('pipeline', '/id/{id}/pipeline')
    config.add_route('location', '/locations/{host}*path')
    config.add_route('modality', '/modalities/{modality}')
    config.add_route('subject', '/subjects/{subject}')
    config.add_route('project', '/projects/{project}')
    config.add_route('user', '/users/{user}')
    config.add_route('search', '/search')
    config.add_route('modalities', '/modalities')
    config.add_route('projects', '/projects')
    config.add_route('users', '/users')
    config.add_request_method(lambda r: Dependencies(), 
        'dependencies', reify=True)
    config.scan()
    return config.make_wsgi_app()

"""
Documentation:
PasteDeploy: http://pythonpaste.org/deploy/
(Handles reading config from file and picking server and app settings)
Waitress: http://waitress.readthedocs.org/en/latest/
(How to start and configure waitress)
"""
