// function definitions

var hasAsParent = function(file, parent) {
    if ('parents' in file) {
        return file.parents.indexOf(parent.location) > -1
    }
    else {return false;}
}

var allParentsIn = function(file, fileHaystack) {
    locationHaystack = fileHaystack.map(function (file) { 
        return file.location; 
    });
    for (var i = 0; i < file.parents.length; i++) {
        if (locationHaystack.indexOf(file.parents[i]) === -1) {
            return false;
        }
    }
    return true;
}

var findExistingParent = function(child, potentialParents) {
    for (var i = 0; i < potentialParents.length; i++) {
        potentialParent = potentialParents[i]
        if ('children' in potentialParent) {
            for (var j = 0; j < potentialParent.children.length; j++) {
                if (potentialParent.children[j] === child) {
                    return potentialParent;
                }
            }
        }
    }
    return null;
}

var findChildrenOfGeneration = function findChildrenOfGeneration (parents, prevGenFiles) {
    prevGenFiles = prevGenFiles.concat(parents)
    var generation = []
    for (var p = 0; p < parents.length; p++) {
        parents[p].children = [];
        for (var f = 0; f < files.length; f++) {
            if ( hasAsParent(files[f], parents[p]) && 
                    allParentsIn(files[f], prevGenFiles)) {
                if (!findExistingParent(files[f], files)) {
                    generation.push(files[f]);
                    parents[p].children.push(files[f]);
                }
            }
        }
    }
    if (generation.length > 0) {
        findChildrenOfGeneration(generation, prevGenFiles);
    }
}

var fileByLocation = function(location, files) {
    for (var f = 0; f < files.length; f++) {
        if (files[f].location === location) {
            return files[f];
        }
    }
}

var addExtraParentLinks = function(links, files) {
    for (var f = 0; f < files.length; f++) {
        existingParent = findExistingParent(files[f], files)
        if ('parents' in files[f]) {
            for (var p = 0; p < files[f].parents.length; p++) {
                parent = fileByLocation(files[f].parents[p], files)
                if (parent != existingParent) {
                    links.push({source: parent, target:files[f]});
                }
            }
        }
    }
}
    
var filesToHierarchy = function(files) {
    var rootfiles = files.filter(function(f){ return !('parents' in f) });
    var root = {path: 'root', children: rootfiles};
    var prevGenFiles = [];
    findChildrenOfGeneration(rootfiles, prevGenFiles);
    return root
}

var shortname = function(path) {
    var fname = path.split(/[\\/]/).pop();
    if (fname.length > 20) {
        return fname.substring(0,7)+'...'+fname.substring(fname.length-10);
    };
    return fname
}

var translate = function(x, y) {
    return 'translate(' + x + ',' + y + ')'
}

window.onload = function() {

//Width and height
var svgWidth = 500;
var svgHeight = 500;
var tooltipfields = ["id", "added", "hostname", "path", "size"]
var fieldTypes = {"added":'datetime', "size":'filesize'}

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
addExtraParentLinks(links, files)

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
                dd = deflist.insert('dd').text(d[field]);
                if (field in fieldTypes) {
                    dd.classed(fieldTypes[field], true);
                }
            }
        }
        makeFieldsHumanReadable();
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

svgcrowbar();

}
