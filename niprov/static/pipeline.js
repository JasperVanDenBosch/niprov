//Width and height
var svgWidth = 500;
var svgHeight = 500;

//Data
var dataset = [ 'raw file', 'transform 1', 'transform 2' ];

//Create SVG element
var svg = d3.select("body")
            .append("svg")
            .attr("width", svgWidth)
            .attr("height", svgHeight);

var rectangles = svg.selectAll("rect")
    .data(dataset)
    .enter()
    .append("rect");

rectangles
    .attr("x", svgWidth/2)
    .attr("y", function(d, i) {
        return 20+i*70;
    })
    .attr("width", 100)
    .attr("height", 50)
    .append("text")
    .text( function(d) { 
        return d;
    });
