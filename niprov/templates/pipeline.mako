<%inherit file="master.mako"/>

<h1>pipeline</h1>

<a class="download" download="provenance_pipeline_${sid}.svg">download pipeline image</a>

<script>var files = ${request.dependencies.getSerializer().serializeList(pipeline.files) | n};</script>
<script type="text/javascript" src="${request.static_url('niprov:static/niprov.js')}"></script>
<script type="text/javascript" src="${request.static_url('niprov:static/pipeline.js')}"></script>
<script type="text/javascript" src="${request.static_url('niprov:static/svg-crowbar.js')}"></script>
