//Width and height
var svgWidth = 500;
var svgHeight = 500;

//Data
var dataset = [ 'raw file', 'transform 1', 'transform 2' ];

//Create SVG element
var svg = d3.select('body')
            .append('svg')
            .attr('width', svgWidth)
            .attr('height', svgHeight);

var groups = svg.selectAll('g')
    .data(dataset)
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
        return d;
    })
    .attr('x', svgWidth/2)
    .attr('y', function(d, i) {
        return 30+i*70;
    });

