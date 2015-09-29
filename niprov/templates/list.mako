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
<th>Id</th>
<th>Acquired</th>
<th>Subject</th>
<th>Protocol</th>
<th>Location</th>
</tr>
</thead>
<tbody>

% for img in images:
   <tr>
        <td><a href="${request.route_url('short',id=img.provenance.get('id'))}">${img.provenance.get('id')}</a></td>
        <td>${img.provenance.get('acquired')}</td>
        <td>${img.provenance.get('subject')}</td>
        <td>${img.provenance.get('protocol')}</td>
        <td>${img.provenance.get('location')}</td>
    </tr>
% endfor

</tbody></table>

</html>
