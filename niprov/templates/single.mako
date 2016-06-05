<%inherit file="master.mako"/>
<%def name="dictAsDefList(dictObject, level=1)">
<dl class="dictfield">
% for k, v in dictObject.items():
    <dt>${k}</dt>
% if isinstance(v, dict):
    <dd class="x">${dictAsDefList(v)}</dd>
% else:
    <dd class="x">${v}</dd>
% endif

% endfor
</dl>
</%def>
<%! import os %>
<h1>${os.path.basename(image.provenance['path'])}</h1>

<a href="${request.route_url('pipeline',id=image.provenance.get('id'))}">view pipeline
    <img class="linkicon" src="${request.static_url('niprov:static/pipeline-link.svg')}" alt="pipeline"/></a>

% if image.getSnapshotFilepath():
    <img class="snapshot" src="${request.static_url(image.getSnapshotFilepath())}" alt="snapshot"/>
% endif


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
        </dt>
% if isinstance(v, dict):
    <dd class="${fieldtype}">${dictAsDefList(v)}</dd>
% else:
    <dd class="${fieldtype}">${v}</dd>
% endif

% endfor
% if 'filesInSeries' in image.provenance:
    <dt>number of files</dt><dd>${len(image.provenance['filesInSeries'])}</dd>
% endif
</dl>

<script type="text/javascript" src="${request.static_url('niprov:static/niprov.js')}"></script>

