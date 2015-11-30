<%inherit file="master.mako"/>

<h1>pipeline</h1>

<script>var files = ${request.dependencies.getSerializer().serializeList(pipeline.files) | n};</script>
<script type="text/javascript" src="${request.static_url('niprov:static/pipeline.js')}"></script>
