var g = $graph_data ;

s = new sigma({graph: g, container: '$container', settings: { defaultNodeColor: '#ec5148'} });
// var filter=new sigma.plugins.filter(s);

s.graph.nodes().forEach(function(n) {
  n.originalColor = n.color;
});
s.graph.edges().forEach(function(e) {
  e.originalColor = e.color;
});

s.startForceAtlas2({worker: true, barnesHutOptimize: false});

s.bind('clickNode', function(e) {
  var nodeId = e.data.node.id,
      toKeep = s.graph.neighbors(nodeId);
  toKeep[nodeId] = e.data.node;

  s.graph.nodes().forEach(function(n) {
    if (toKeep[n.id])
      n.color = n.originalColor;
    else
      n.color = '#eee';
  });

  s.graph.edges().forEach(function(e) {
    if ((toKeep[e.source] && e.target===nodeId)||(e.source===nodeId && toKeep[e.target]))
      e.color = e.originalColor;
    else
      e.color = '#eee';
  });
  // filter.undo("neighbors")
  //             .neighborsOf(nodeId,"neighbors")
  //             .apply();
  s.refresh();
});

s.bind('clickStage', function(e) {
  s.graph.nodes().forEach(function(n) {
    n.color = n.originalColor;
  });

  s.graph.edges().forEach(function(e) {
    e.color = e.originalColor;
  });
  // filter.undo("neighbors")
  s.refresh();
});
