<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="neuroimaging provenance">
    <meta name="author" content="Jasper J.F. van den Bosch">
    <link rel="shortcut icon" href="${request.static_url('niprov:static/niprov.ico')}">
    <link rel="stylesheet" type="text/css" href="${request.static_url('niprov:static/master.css')}">
    <link rel="stylesheet" type="text/css" href="${request.static_url('niprov:static/pipeline.css')}">
    <script type="text/javascript" src="${request.static_url('niprov:static/d3.min.js')}"></script>
    <script type="text/javascript" src="${request.static_url('niprov:static/jquery-2.1.4.min.js')}"></script>
    <script type="text/javascript" src="${request.static_url('niprov:static/moment.min.js')}"></script>
    <title>Provenance</title>
  </head>

  <body>
        <p id="header">
            <a href="${request.route_url('home')}">
                <img id="logo" src="${request.static_url('niprov:static/niprov.svg')}"/>
            </a>
            <a href="${request.route_url('latest')}">latest</a>
            <a href="${request.route_url('modalities')}">modalities</a>
            <a href="${request.route_url('projects')}">projects</a>
            <a href="${request.route_url('users')}">users</a>
            <a href="${request.route_url('stats')}">statistics</a>
            <a href="http://niprov.readthedocs.org/en/latest/">documentation</a>
        </p>

        <form action="${request.route_url('search')}">
            <input type="text" name="text" 

% if not context.get('searchtext', None) is None:
            value="${searchtext}"
% else:
            placeholder="Search..."
% endif
            required>

            <input type="submit" value="Search">
        </form>

        ${self.body()}

  </body>
</html>
