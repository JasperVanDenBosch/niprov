from pyramid.config import Configurator
import waitress

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
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()
