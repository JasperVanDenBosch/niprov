<html>
<head>
<style>
html {font-family:arial;}
td {padding: 10px;}
tr:hover {background-color:lavender;}
dt {color: dark-grey; font-style: italic; background-color:lavender; padding: 10px;}
dd {padding: 10px;}
</style>
<title>Provenance</title>
</head>
<h1>Provenance</h1>

<dl>
% for k, v in provenance.items():
    <dt>${k}</dt><dd>${v}</dd>
% endfor
</dl>

</html>
