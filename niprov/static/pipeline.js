
// function definitions
var filesToHierarchy = function(files) {
    var root = {path: 'root'};
    var rootfiles = files.filter(function(f){ return !('parents' in f) })
    rootfiles.forEach(function findChildrenRecursively (file, i, arr) {
        var hasParent = function(file, parentname) {
            if ('parents' in file) {
                return file.parents.indexOf(parentname) > -1
            }
            else {return false;}
        };
        var children = files.filter(function(o){ 
            return hasParent(o, file.location) });
        children.forEach(findChildrenRecursively)
        file.children = children
    });
    if(rootfiles.length > 0) {
        root.children = rootfiles;
    };
    return root
};
var shortname = function(path) {
    var fname = path.split(/[\\/]/).pop();
    if (fname.length > 20) {
        return fname.substring(0,7)+'...'+fname.substring(fname.length-10);
    };
    return fname
};
var translate = function(x, y) {
    return 'translate(' + x + ',' + y + ')'
};

//Width and height
var svgWidth = 500;
var svgHeight = 500;

//Data
var files = [{"added": "2015-10-20T20:50:33.996245", "script": null, "acquired": "2015-03-09T13:07:03.000000", "hostname": "gram", "transformation": "trans1", "transient": true, "parents": ["gram:/home/jasper/Projects/niprov/testdata/eeg/stub.cnt"], "location": "gram:/p/child1.txt", "path": "/p/child1.txt", "id": "Vspqnf", "subject": "Jane Doe"}, {"added": "2015-10-20T20:49:03.777477", "hash": "f9ccd1b4312d9ebd3daf727054815276", "dimensions": [32, 2080], "created": "2015-03-09T20:19:19.367602", "acquired": "2015-03-09T13:07:03.000000", "hostname": "gram", "transient": false, "location": "gram:/home/jasper/Projects/niprov/testdata/eeg/stub.cnt", "path": "/home/jasper/Projects/niprov/testdata/eeg/stub.cnt", "size": 492581, "id": "VR55dC", "subject": "Jane Doe"}, {"added": "2015-10-20T20:51:00.178131", "script": null, "acquired": "2015-03-09T13:07:03.000000", "hostname": "gram", "transformation": "trans2", "transient": true, "parents": ["gram:/p/child1.txt"], "location": "gram:/p/b/child2.txt", "path": "/p/b/child2.txt", "id": "toGp6R", "subject": "Jane Doe"}, {"added": "2015-10-20T20:52:00.178131", "script": null, "acquired": "2015-03-09T13:07:03.000000", "hostname": "gram", "transformation": "trans2", "transient": true, "parents": ["gram:/p/child1.txt"], "location": "gram:/p/b/child3.txt", "path": "/p/b/child3.txt", "id": "J7yUxi", "subject": "Jane Doe"}];

//Create SVG element
var svg = d3.select('body')
            .append('svg')
            .attr('width', svgWidth)
            .attr('height', svgHeight)
                .append('g')
                .attr('transform',translate(50,50));

var tree = d3.layout.tree()
    .size([svgHeight-100, svgWidth-100]);

var root = filesToHierarchy(files)
var nodes = tree.nodes(root)
var links = tree.links(nodes)

var nodeGroup = svg.selectAll('g.node')
    .data(nodes)
    .enter()
    .append('g')
        .attr('class','node')
        .attr('transform', function(d) {return translate(d.x, d.y)});

nodeGroup
    .append('rect')
    .attr('width', 100)
    .attr('height', 30);

nodeGroup
    .append('text')
    .text( function(d) { 
        return shortname(d.path);
    });

svg.selectAll("path.link")
    .data(links)
    .enter()
    .append('path')
        .attr('class','link')
        .attr('d', d3.svg.diagonal());



