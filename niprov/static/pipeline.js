// function definitions
var filesToHierarchy = function(files) {
    var root = {path: 'root'};
    var rootfiles = files.filter(function(f){ return !('parents' in f) })
    var hasAsParent = function(file, parent) {
        if ('parents' in file) {
            return file.parents.indexOf(parent.location) > -1
        }
        else {return false;}
    };
    var allParentsInPreviousGenerations = function(file, prevGenFiles) {
        //check each parent in prevGenFiles
    }
    if(rootfiles.length > 0) {
        root.children = rootfiles;
    };
    var prevGenFiles = [];
    (function findChildrenOfGeneration (parents, prevGenFiles) {
        prevGenFiles += parents
        parents.forEach(function (parent, p, parents) {
            parent.children = [];
            files.forEach(function (file) {
                if hasAsParent(file, parent) &&
                    allParentsInPreviousGenerations(file, prevGenFiles)
                {
                    //file.inmediateParent = parent;
                    children.append(file);
                    parent.children.append(child);
                }
            });
        });
        findChildrenOfGeneration(children, prevGenFiles);
    }(rootfiles, prevGenFiles));
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
var tooltipfields = ["id", "added", "hostname", "path", "size"]

// Creat toolip container
var tooltipDiv = d3.select('body')
    .append('div')
    .attr('class','tooltip')

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
    .append('circle')
    .attr('r', 5);

nodeGroup
    .append('text')
    .text( function(d) { 
        return shortname(d.path);
    })
    .attr('transform',translate(10,5))
    .on("mouseover", function (d) {
        
        var matrix = this.getScreenCTM()
                .translate(+this.getAttribute("cx"),
                         +this.getAttribute("cy"));
        tooltipDiv
            .style("opacity", "1")
            .style("left", 
                   (window.pageXOffset + matrix.e) + "px")
            .style("top",
                   (window.pageYOffset + matrix.f + 30) + "px");
        var deflist = tooltipDiv.insert('dl');
        for (i = 0; i < tooltipfields.length; ++i) {
            var field = tooltipfields[i]
            if (field in d) {
                deflist.insert('dt').text(field);
                deflist.insert('dd').text(d[field]);
            }
        }

        
    })
    .on("mouseout", function () {
        tooltipDiv.selectAll('dl').remove()
        return tooltipDiv.style("opacity", "0");
    });

svg.selectAll("path.link")
    .data(links)
    .enter()
    .append('path')
        .attr('class','link')
        .attr('d', d3.svg.diagonal());





