<%inherit file="master.mako"/>

<h1>${len(images)} files</h1>

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
        <td><a href="${request.route_url('short',id=img.provenance.get('id'))}">${img.provenance.get('id')}</a>
            <a href="${request.route_url('pipeline',id=img.provenance.get('id'))}">
                <img class="linkicon" src="${request.static_url('niprov:static/pipeline-link.svg')}" alt="pipeline"/></a></td>
        <td>${img.provenance.get('acquired')}</td>
        <td><a href="${request.route_url('subject',subject=img.provenance.get('subject'))}">${img.provenance.get('subject')}</a></td>
        <td>${img.provenance.get('protocol')}</td>
        <td><a href="${request.route_url('location',host=img.provenance.get('hostname'),path=img.provenance.get('path'))}">${img.provenance.get('location')}</a></td>
    </tr>
% endfor

</tbody></table>


