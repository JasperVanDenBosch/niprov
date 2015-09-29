<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="neuroimaging provenance">
    <meta name="author" content="Jasper J.F. van den Bosch">
    <link rel="shortcut icon" href="${request.static_url('niprov:static/pyramid-16x16.png')}">

    <title>Provenance</title>

    <style>
    html {font-family:arial;}
    td {padding: 10px;}
    tr:hover {background-color:lavender;}
    dt {color: dark-grey; font-style: italic; background-color:lavender; padding: 10px;}
    dd {padding: 10px;}
    </style>



  </head>

  <body>



        <p id="header">
            <a href="${request.route_url('home')}">home</a>
            <a href="${request.route_url('latest')}">latest</a>
            <a href="${request.route_url('stats')}">statistics</a>
            <a href="http://niprov.readthedocs.org/en/latest/">documentation</a>
        </p>


        ${self.body()}



  </body>
</html>
