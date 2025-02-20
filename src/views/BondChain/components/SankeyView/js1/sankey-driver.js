// Author: Ming Qin (https://github.com/QinMing)
// Copyright 2015 Yahoo Inc.
// This file is licensed under the MIT License. See LICENSE in the project root for terms

/*global d3*/
/* eslint-disable */
import './sankey.js'
class SankeyDriver {
  constructor() {
    this.sankey = d3.sankey();
    this.formatNumber = d3.format(",");
    // this.color = d3.scaleOrdinal(d3.schemeCategory20);
    this.graph = null;
    this.width = null;
    this.height = null;
    this.tooltips = [];
    this.tooltipEnable = true;
    this.tooltipContainer = null;
    this.tbody = null;
  }

  prepare(canvas, sz, margin) {
    this.width = sz.width - margin.left - margin.right;
    this.height = sz.height - margin.top - margin.bottom;

    this.graph = canvas
      .append('svg')
        .attr("width", sz.width)
        .attr("height", sz.height)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    this.tooltipContainer = canvas
      .append('div')
        .attr('id', 'tooltip-container');

    this.tbody = this.tooltipContainer
      .append('table')
        .attr('class', 'tooltip')
      .append('tbody');
  }

  draw(inputdata) {
    const self = this;
    console.log('inputdata:', inputdata)
    this.sankey
      .nodeWidth(40)
      .nodePadding(10)
      .size([this.width, this.height]);

    this.sankey.nodes(inputdata.nodes)
      .flows(inputdata.flows)
      .layout(32);
    drawNode(this.sankey.nodes());
    drawLink(this.sankey.links());

    function drawNode(nodes) {
      var group = self.graph.selectAll('g#node-group').data([0]);
      
      group.enter().append('g').attr("id", "node-group");
      var node = group.selectAll("g.node").data(nodes);
      console.log('group:', nodes)
      node.exit().remove();
      var nodeEnter = node.enter().append("g")
        .attr("class", "node")
        .on("mouseover", self.funcMouseover)
        .on("mouseout", self.funcMouseout)
        .on('mousemove', self.funcMousemove)
        .on('dblclick', self.funcTooltipToggle)
        .call(d3.drag()
        .on("start", function(event, d) {
          d3.event.sourceEvent.stopPropagation();
          this.parentNode.appendChild(this);
        })
        .on("drag", function(event, d) {
          var newY = event.y;
          d.y = newY;
          d3.select(this).attr("transform",
            "translate(" + (
              d.x = Math.max(0, Math.min(self.width - d.dx, event.x))
            ) + "," + (
              newY
            ) + ")");
          self.sankey.relayout();
          self.graph.select('g#normal').selectAll('path').attr("d", self.sankey.link());
          self.graph.select('g#highlight').selectAll('path').attr("d", self.sankey.link());
        })
      );
      // Append rectangle for each node
      nodeEnter.append("rect")
        .attr("height", function (d) {
          return 12;
        })
        .attr("width", function (d) {
          return d.dy / 5;
        })
        .attr("rx", 4)
        .attr("ry", 4)
        .attr("fill", "white")
        .attr("stroke", "lightgray")
        .attr("stroke-width", 1);
      const data = [
        {
            "name": "东海证券股份温妍超",
            "time_dl": "2023-12-06 16:44:13",
            "volume": 10,
            "price": 110.36,
            "xy_coordinates": {
                "x": 50.0,
                "y": 0
            },
            "color": [147, 209, 188]
        },
        {
            "name": "长线资本基金孙姣",
            "time_dl": "2023-12-06 16:44:13",
            "volume": 10,
            "price": 110.36,
            "xy_coordinates": {
                "x": 70.0,
                "y": 0
            },
            "color": [209, 168, 147]
        },
        {
            "name": "华源证券股份钱淑雯",
            "time_dl": "2023-12-07 13:33:23",
            "volume": 10,
            "price": 110.51,
            "xy_coordinates": {
                "x": 93.55271621933369,
                "y": 0
            },
            "color": [147, 209, 147]
        },
        {
            "name": "鄂尔多斯银行郭宁",
            "time_dl": "2023-12-07 13:35:23",
            "volume": 10,
            "price": 110.53,
            "xy_coordinates": {
                "x": 113.55271621933369,
                "y": 0
            },
            "color": [209, 188, 147]
        },
        {
            "name": "粤开证券股份周荃",
            "time_dl": "2023-12-22 13:54:34",
            "volume": 10,
            "price": 112.83,
            "xy_coordinates": {
                "x": 847.3842802296235,
                "y": 0
            },
            "color": [209, 147, 147]
        }
      ];
      node.select('rect')
        .attr("height", function (d) {
          return 12;
        })
        .attr("width", function (d) {
          return d.dy / 5;
        })
        .attr("rx", 4)
        .attr("ry", 4)
        .attr("fill", "white")
        .attr("stroke", "lightgray")
        .attr("stroke-width", 1);
      node.selectAll("circle")
        .data(data)
        .enter().append("circle")
        .attr("cx", (d, i) => 7 + i * 10)
        .attr("cy", 6)
        .attr("r", 5)
        .attr("fill", d => `rgb(${d.color[0]}, ${d.color[1]}, ${d.color[2]})`);
      node.select("text")
        .attr("x", -6)
        .attr("y", function (d) {
          return 20;
        })
        .attr("dy", ".35em")
        .attr("text-anchor", "end")
        .attr("transform", null)
        .text(function (d) {
          return d.disp;
        })
        .filter(function (d) {
          return d.x < self.width / 2;
        })
        .attr("x", 6 + self.sankey.nodeWidth())
        .attr("text-anchor", "start");
    }

    function drawLink(data) {
      var group = self.graph.selectAll('g#normal').data([0]);
      group.enter().insert("g", ":first-child").attr('id', 'normal');
      var link = group.selectAll('path.link').data(data);
      link.exit().remove();

      link.enter().append("path")
        .attr("class", "link")
        .on("mouseover", self.funcMouseover)
        .on("mouseout", self.funcMouseout)
        .on('mousemove', self.funcMousemove)
        .on('dblclick', self.funcTooltipToggle);
      link
        .attr("d", self.sankey.link())
        .style("stroke-width", function (d) {
          return 3;
        })
        .sort(function (a, b) {
          return b.dy - a.dy;
        });
    }
  }

  funcMouseover(d) {
    this.sankey.dflows(d.flows);
    this.drawDLink(this.sankey.dlinks());
    this.updateTooltip(d);
    this.tooltipContainer.style('display', 'block');
  }

  funcMouseout() {
    this.graph.selectAll("g#highlight").remove();
    this.tooltipContainer.style('display', 'none');
  }

  funcMousemove() {
    this.tooltipContainer
      .style('top', d3.event.clientY + 'px')
      .style('left', d3.event.clientX + 'px');
  }

  funcTooltipToggle(d){
    this.tooltipEnable = !this.tooltipEnable;
    this.updateTooltip(d);
  }

  drawDLink(data) {
    return this.graph.insert("g", ":first-child")
      .attr('id', 'highlight')
      .selectAll('path')
      .data(data)
      .enter()
      .append("path")
        .attr("class", "link highlight")
        .attr("d", this.sankey.link())
        .style("stroke-width", function (d) {
          return 10;
        })
        .sort(function (a, b) {
          return b.dy - a.dy;
        });
  }

  updateTooltip(d) {
    this.tooltips = [d.tooltip];
    if (this.tooltipEnable){
      d.flows.forEach(function(f){
        this.tooltips.push(f.tooltip);
      });
    }

    this.tbody.selectAll('*').remove();
    this.tooltips.forEach(function(tip){
      var tr = this.tbody.append('tr');
      tr.append('td')
        .attr('class', 'name')
        .classed('head', 'head' in tip)
        .html(tip.name + " → " + tip.name + " → " + tip.name);
      tr.append('td')
        .attr('class', 'value')
        .classed('head', 'head' in tip)
        .html(tip.value);
    });
  }
}

export default SankeyDriver;
