<%inherit file="master.mako"/>

<h1>${categoryPlural}</h1>

<ul>
% for item in items:
    <li>
        <a href="${request.route_url(category,**{category:item})}">${item}</a>
    </li>
% endfor
</ul>




