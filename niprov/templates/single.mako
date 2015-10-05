<%inherit file="master.mako"/>
<%! import os %>
<h1>${os.path.basename(image.provenance['path'])}</h1>

<dl>
% for k, v in image.provenance.items():
    <dt>${k}<a class="help" href="http://niprov.readthedocs.org/en/latest/provenance-fields.html#${k.lower()}">?</a>
        </dt><dd>${v}</dd>
% endfor
% if 'filesInSeries' in image.provenance:
    <dt>number of files</dt><dd>${len(image.provenance['filesInSeries'])}</dd>
% endif
</dl>

