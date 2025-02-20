import * as d3 from 'd3';

function renderChart(tangleLayout, svg, options) {
  svg.selectAll(".link")
     .data(tangleLayout.bundles)
     .enter().append("g")
     .attr("class", "link")
     .selectAll("path")
     .data(b => b.links)
     .enter().append("path")
     .attr("d", l => {
         const d = `M${l.xt} ${l.yt} L${l.xb} ${l.yt}`;
         return d;
     })
     .attr("stroke", (d, i) => options.color(tangleLayout.bundles[i], i))
     .attr("stroke-width", 2);

  svg.selectAll(".node")
     .data(tangleLayout.nodes)
     .enter().append("circle")
     .attr("class", "node")
     .attr("cx", d => d.xy_coordinates.x)
     .attr("cy", d => d.xy_coordinates.y + 50)
     .attr("r", 7)
     .attr("fill", d => `rgb(${d.color[0]}, ${d.color[1]}, ${d.color[2]})`)
     .attr("stroke-width", 2);

  svg.selectAll(".label")
     .data(tangleLayout.nodes)
     .enter().append("text")
     .attr("class", "label")
     .attr("x", d => d.xy_coordinates.x)
     .attr("y", d => d.xy_coordinates.y + 50)
     .attr("dy", "-1em")
     .attr("text-anchor", "middle")
     .text(d => d.name.slice(-2))
     .style("font-size", "8px");
}

d3.json("data_chain.json").then(function(data) {
  const svg = d3.select("#chart");
  const options = {
    color: (b, i) => i % 2 === 0 ? "blue" : "blue"
  };
  renderChart(data, svg, options);
}).catch(function(error) {
  console.error("Error loading the JSON file:", error);
});

export { renderChart };
