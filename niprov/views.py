from pyramid.view import view_config
import os


@view_config(route_name='home', renderer='templates/home.mako')
def home(request):
    return {'project': 'niprov'}

@view_config(route_name='latest', renderer='templates/list.mako')
def latest(request):
    repository = request.dependencies.getRepository()
    return {'images':repository.latest()}

@view_config(route_name='subject', renderer='templates/list.mako')
def subject(request):
    subj = request.matchdict['subject']
    repository = request.dependencies.getRepository()
    return {'images':repository.bySubject(subj)}

@view_config(route_name='short', renderer='templates/single.mako')
def short(request):
    sid = request.matchdict['id']
    repository = request.dependencies.getRepository()
    return {'image':repository.byId(sid)}

@view_config(route_name='location', renderer='templates/single.mako')
def location(request):
    path = os.sep + os.path.join(*request.matchdict['path'])
    loc = request.matchdict['host'] + ':' + path
    repository = request.dependencies.getRepository()
    return {'image':repository.byLocation(loc)}

@view_config(route_name='stats', renderer='templates/stats.mako')
def stats(request):
    repository = request.dependencies.getRepository()
    return {'stats':repository.statistics()}

