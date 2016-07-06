from pyramid.view import view_config
import os
import niprov.searching as searching
from pyramid.httpexceptions import HTTPNotFound


@view_config(route_name='home', renderer='templates/home.mako')
def home(request):
    return {}

@view_config(route_name='latest', renderer='templates/list.mako')
def latest(request):
    repository = request.dependencies.getRepository()
    return {'images':repository.latest()}

@view_config(route_name='short', renderer='templates/single.mako')
def short(request):
    sid = request.matchdict['id']
    repository = request.dependencies.getRepository()
    query = request.dependencies.getQuery()
    image = repository.byId(sid)
    if not image:
        raise HTTPNotFound
    return {'image': image, 'copies': query.copiesOf(image)}

@view_config(route_name='location', renderer='templates/single.mako')
def location(request):
    path = os.sep + os.path.join(*request.matchdict['path'])
    loc = request.matchdict['host'] + ':' + path
    query = request.dependencies.getQuery()
    image = query.byLocation(loc)
    if not image:
        raise HTTPNotFound
    return {'image': image, 'copies': query.copiesOf(image)}

@view_config(route_name='stats', renderer='templates/stats.mako')
def stats(request):
    repository = request.dependencies.getRepository()
    return {'stats':repository.statistics()}

@view_config(route_name='pipeline', renderer='templates/pipeline.mako')
def pipeline(request):
    sid = request.matchdict['id']
    files = request.dependencies.getRepository()
    pipeline = request.dependencies.getPipelineFactory()
    targetFile = files.byId(sid)
    if not targetFile:
        raise HTTPNotFound
    return {'pipeline':pipeline.forFile(targetFile), 'sid':sid}

@view_config(route_name='subject', renderer='templates/list.mako')
def subject(request):
    subj = request.matchdict['subject']
    query = request.dependencies.getQuery()
    return {'images':query.bySubject(subj)}

@view_config(route_name='project', renderer='templates/list.mako')
def project(request):
    project = request.matchdict['project']
    query = request.dependencies.getQuery()
    return {'images':query.byProject(project)}

@view_config(route_name='user', renderer='templates/list.mako')
def user(request):
    user = request.matchdict['user']
    query = request.dependencies.getQuery()
    return {'images':query.byUser(user)}

@view_config(route_name='modality', renderer='templates/list.mako')
def modality(request):
    modality = request.matchdict['modality']
    query = request.dependencies.getQuery()
    return {'images':query.byModality(modality)}

@view_config(route_name='search', renderer='templates/list.mako')
def search(request):
    text = request.GET['text']
    results = searching.search(text, request.dependencies)
    return {'images':results, 'searchtext':text}

@view_config(route_name='modalities', renderer='templates/category.mako')
def modalities(request):
    query = request.dependencies.getQuery()
    return {'category':'modality', 'categoryPlural':'modalities', 
            'items':query.allModalities()}

@view_config(route_name='projects', renderer='templates/category.mako')
def projects(request):
    query = request.dependencies.getQuery()
    return {'category':'project', 'categoryPlural':'projects', 
            'items':query.allProjects()}

@view_config(route_name='users', renderer='templates/category.mako')
def users(request):
    query = request.dependencies.getQuery()
    return {'category':'user', 'categoryPlural':'users', 
            'items':query.allUsers()}


