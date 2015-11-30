<%inherit file="master.mako"/>
<%! import os %>
<h1>${os.path.basename(image.provenance['path'])}</h1>

<a href="${request.route_url('pipeline',id=image.provenance.get('id'))}">view pipeline
    <img class="linkicon" src="${request.static_url('niprov:static/pipeline-link.svg')}" alt="pipeline"/></a>

<dl class="details">
% for k, v in image.provenance.items():
<%
    if k in ['added', 'acquired', 'created']:
        fieldtype = 'datetime'
    elif k in ['size']:
        fieldtype = 'filesize'
    else:
        fieldtype = 'general'
%>
    <dt>${k}<a class="help" href="http://niprov.readthedocs.org/en/latest/provenance-fields.html#${k.lower()}">?</a>
        </dt><dd class="${fieldtype}">${v}</dd>
% endfor
% if 'filesInSeries' in image.provenance:
    <dt>number of files</dt><dd>${len(image.provenance['filesInSeries'])}</dd>
% endif
</dl>

<script type="text/javascript" src="${request.static_url('niprov:static/niprov.js')}"></script>

