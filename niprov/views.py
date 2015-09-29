from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/home.mako')
def home(request):
    return {'project': 'niprov'}

@view_config(route_name='latest', renderer='templates/list.mako')
def latest(request):
    repository = request.dependencies.getRepository()
    return {'images':repository.latest()}

@view_config(route_name='short', renderer='templates/single.mako')
def short(request):
    sid = request.matchdict['id']
    repository = request.dependencies.getRepository()
    return {'image':repository.byId(sid)}

@view_config(route_name='stats', renderer='templates/stats.mako')
def stats(request):
    repository = request.dependencies.getRepository()
    return {'stats':repository.statistics()}
