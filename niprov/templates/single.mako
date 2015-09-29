<%inherit file="master.mako"/>
<h1>Provenance</h1>

<dl>
% for k, v in image.provenance.items():
    <dt>${k}</dt><dd>${v}</dd>
% endfor
% if 'filesInSeries' in image.provenance:
    <dt>number of files</dt><dd>${len(image.provenance['filesInSeries'])}</dd>
% endif
</dl>

