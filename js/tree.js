var width = 960, 
    height =600
    
var svg = d3.select("#tree-div").append("svg")
    .attr("width",width)
    .attr("height",height)
     .append("g")
    .attr("transform", "translate(20,20)");
    
var tree = d3.layout.cluster()
    .size([height, width - 160]);

var diagonal = d3.svg.diagonal()
    .projection(function(d) { return [d.y, d.x]; });

var data=$python_data;

var root = {};

// Create nodes for each unique source and target.
  data.forEach(function(link) {
    var parent = link.source = nodeByName(link.source),
        child = link.target = nodeByName(link.target);
    if (parent.children) parent.children.push(child);
    else parent.children = [child];
  });

  // Extract the root node.
  var root = data[0].source;

  function nodeByName(name) {
    return root[name] || (root[name] = {name: name});
  }
  
  var nodes = tree.nodes(root);

  var link = svg.selectAll(".link")
      .data(tree.links(nodes))
    .enter().append("path")
      .attr("class", "link")
      .attr("d", diagonal);

  var node = svg.selectAll(".node")
      .data(nodes)
        .enter().append("g")
      .attr("class", "node")
      .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; })

  node.append("circle")
      .attr("r", 2.5);

  node.append("text")
      .attr("dy", 3)
      .attr("x", function(d) { return d.children ? -8 : 8; })
      .style("text-anchor", function(d) { return d.children ? "end" : "start"; })
      .text(function(d) { return d.name});