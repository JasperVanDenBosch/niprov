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


<table>
<thead>
<tr>
<th>Acquired</th>
<th>Subject</th>
<th>Protocol</th>
<th>Path</th>
</tr>
</thead>
<tbody>

% for row in rows:
   <tr><td>{0[acquired]}</td><td>{0[subject]}</td><td>{0[protocol]}</td><td>{1}</td></tr>
% endfor

</tbody></table>

</html>
