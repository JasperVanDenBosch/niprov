//Width and height
var svgWidth = 500;
var svgHeight = 500;

//Data
var files = [{"added": "2015-10-20T20:50:33.996245", "script": null, "acquired": "2015-03-09T13:07:03.000000", "hostname": "gram", "transformation": "trans1", "transient": true, "parents": ["gram:/home/jasper/Projects/niprov/testdata/eeg/stub.cnt"], "location": "gram:/p/child1.txt", "path": "/p/child1.txt", "id": "Vspqnf", "subject": "Jane Doe"}, {"added": "2015-10-20T20:49:03.777477", "hash": "f9ccd1b4312d9ebd3daf727054815276", "dimensions": [32, 2080], "created": "2015-03-09T20:19:19.367602", "acquired": "2015-03-09T13:07:03.000000", "hostname": "gram", "transient": false, "location": "gram:/home/jasper/Projects/niprov/testdata/eeg/stub.cnt", "path": "/home/jasper/Projects/niprov/testdata/eeg/stub.cnt", "size": 492581, "id": "VR55dC", "subject": "Jane Doe"}, {"added": "2015-10-20T20:51:00.178131", "script": null, "acquired": "2015-03-09T13:07:03.000000", "hostname": "gram", "transformation": "trans2", "transient": true, "parents": ["gram:/p/child1.txt"], "location": "gram:/p/b/child2.txt", "path": "/p/b/child2.txt", "id": "toGp6R", "subject": "Jane Doe"}];

//Create SVG element
var svg = d3.select('body')
            .append('svg')
            .attr('width', svgWidth)
            .attr('height', svgHeight);

var groups = svg.selectAll('g')
    .data(files)
    .enter()
    .append('g');

groups
    .append('line')
    .attr('x1', svgWidth/2)
    .attr('y1', function(d, i) {
        return i*70;
    })
    .attr('x2', svgWidth/2)
    .attr('y2', function(d, i) {
        return 20+i*70;
    })

groups
    .append('rect')
    .attr('x', svgWidth/2)
    .attr('y', function(d, i) {
        return 20+i*70;
    })
    .attr('width', 100)
    .attr('height', 50)

groups
    .append('text')
    .text( function(d) { 
        return d.id;
    })
    .attr('x', svgWidth/2)
    .attr('y', function(d, i) {
        return 30+i*70;
    });

