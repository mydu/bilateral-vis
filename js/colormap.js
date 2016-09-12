var world = $worldmapdata;
var partition= $partition;
var partition_map={}
partition.forEach(function(d){
	partition_map[d.iso3c]=d.partition
})

var community=d3.set(partition.map(function(d){return d.partition;})).values()
var svg = d3.select("#graph-svg");
var color = d3.scale.category20();
var color=['#2079b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a']
// var color=['#a6cee3',
//  '#2079b4',
//  '#b0dd8b',
//  '#36a12e',
//  '#fb9898',
//  '#e31b1c',
//  '#fdbe6f',
//  '#ff8001',
//  '#c8afd5',
//  '#6c409a']
var projection = d3.geo.mercator();

var path = d3.geo.path()
   .projection(projection);

d3.select("#graph-svg").append("g")
    .attr("id","mapCountries")
    .attr("transform","translate(0,50)");

d3.select("#mapCountries").selectAll(".pathCountry")
        .data(world.features)
      	.enter().append("path")
        .attr("class", "pathCountry")
        .attr("d", path)
        .style("fill", function(d,i){
        	if(partition_map[d.id]!==undefined){
        		return color[partition_map[d.id]];
        	} 
         })
        .append("svg:title")
        .text(function(d) {return d.id});

d3.select("#graph-svg").append("g")
    .attr("id","legend")
	.attr("transform","translate(20,360)")

var legend=d3.select("#legend")
			  .selectAll("g")
			  .data(community)
			  .enter().append("g")
			  .attr("transform",function(d,i){return "translate(0,"+15*i+")"})

legend.append("rect")
	  .attr("width",20)
	  .attr("height",10)
	  .attr("fill",function(d,i){return color[i]})


legend.append("text")
	  .attr("x",25)
	  .attr("y",10)
	  .text(function(d,i){return (i+1);})