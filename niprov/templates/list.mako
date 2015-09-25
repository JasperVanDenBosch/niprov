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

% for img in provenance:
   <tr>
        <td>${img.provenance.get('acquired')}</td>
        <td>${img.provenance.get('subject')}</td>
        <td>${img.provenance.get('protocol')}</td>
        <td>${img.provenance.get('path')}</td>
    </tr>
% endfor

</tbody></table>

</html>
