<%inherit file="master.mako"/>

<h1>Statistics</h1>

<dl>
% for k, v in stats.items():
    <dt>${k}</dt><dd>${v}</dd>
% endfor
</dl>
