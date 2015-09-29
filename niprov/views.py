from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/mytemplate.mako')
def home(request):
    return {'project': 'niprov'}

@view_config(route_name='latest', renderer='templates/list.mako')
def latest(request):
    repository = request.dependencies.getRepository()
    return {'images':repository.latest()}
