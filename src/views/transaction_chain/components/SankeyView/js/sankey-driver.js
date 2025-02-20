// Author: Ming Qin (https://github.com/QinMing)
// Copyright 2015 Yahoo Inc.
// This file is licensed under the MIT License. See LICENSE in the project root for terms

/*global d3*/

var SankeyDriver = function (){
  var sankey = d3.sankey();
  var formatNumber = d3.format(","); //(",.2f");
  var color = d3.scale.category20c();
  var graph, width, height;
  var tooltips = [];
  var tooltipEnable = true;
  var tooltipContainer, tbody;

  this.prepare = function (canvas, sz, margin) {
    width = sz.width - margin.left - margin.right;
    height= sz.height - margin.top - margin.bottom;

    graph = canvas
      .html('')
      .append('svg')
        .attr("width", sz.width)
        .attr("height", sz.height)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    tooltipContainer = canvas
      .append('div')
        .attr('id', 'tooltip-container');

    tbody = tooltipContainer
      .append('table')
        .attr('class', 'tooltip')
      .append('tbody');
  };

  this.draw = function (inputdata) {

    sankey
      .nodeWidth(40)
      .nodePadding(10)
      .size([width, height]);

    sankey.nodes(inputdata.nodes)
      .flows(inputdata.flows)
      .layout(32);

    drawNode(sankey.nodes());
    drawLink(sankey.links());

    function drawNode(nodes) {
      var group = graph.selectAll('g#node-group').data([0]);
      group.enter().append('g').attr("id", "node-group");
      var node = group.selectAll("g.node").data(nodes);
      node.exit().remove();

      var nodeEnter = node.enter().append("g")
        .attr("class", "node")
        .on("mouseover", funcMouseover)
        .on("mouseout", funcMouseout)
        .on('mousemove', funcMousemove)
        .on('dblclick', funcTooltipToggle)
        .call(d3.behavior.drag()
          .origin(function (d) {
            return d;
          })
          .on("dragstart", function () {
            d3.event.sourceEvent.stopPropagation();
            this.parentNode.appendChild(this);
          })
          .on("drag", function dragmove(d) {
            console.log("dragmove", d)
            var newY = d3.event.y;
            d.y = newY
            d3.select(this).attr("transform",
              "translate(" + (
                d.x = Math.max(0, Math.min(width - d.dx, d3.event.x))
              ) + "," + (
                newY
              ) + ")");
            // d3.select(this).attr("transform",
            //   "translate(" + (
            //     d.x = Math.max(0, Math.min(width - d.dx, d3.event.x))
            //   ) + "," + (
            //     d.y = Math.max(0, Math.min(height - d.dy, d3.event.y))
            //   ) + ")");
            sankey.relayout();
            graph.select('g#normal').selectAll('path').attr("d", sankey.link());
            graph.select('g#highlight').selectAll('path').attr("d", sankey.link());
          })
        );
      nodeEnter.append("rect");//.append('title');
      // nodeEnter.append("text");

      node
        .attr("transform", function (d) {
          console.log("transform", d)
          return "translate(" + d.x + "," + d.y + ")";
          // return "translate(" + d.x + "," + (d.y + d.dy / 2 - 2) + ")";
        });

      // node.select('rect')
      //   .attr("height", function (d) {
      //     return 5;
      //   })
      //   .attr("width", function (d) {
      //     return d.dy / 5
      //   })
      //   .style("fill", function (d) {
      //     if (!d.color){
      //       d.color = color(d.disp);
      //     }
      //     return d.color;
      //   })
      //   .style("stroke", function (d) {
      //     return d3.rgb(d.color).darker(2);
      //   })
      //   .select("title")
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
      ]
      node.select('rect')
        .attr("height", function (d) {
          return 12;
        })
        .attr("width", function (d) {
          return d.dy / 5
        })
        .attr("rx", 4) // 水平方向的圆角半径
        .attr("ry", 4) // 垂直方向的圆角半径
        // .style("fill", function (d) {
        //   if (!d.color){
        //     d.color = color(d.disp);
        //   }
        //   return d.color;
        // })
        // .style("stroke", function (d) {
        //   return d3.rgb(d.color).darker(2);
        // })
        // .attr("fill", "white")
        // .select("title")
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
          console.log("text", d)
          return 20;
        })
        .attr("dy", ".35em")
        .attr("text-anchor", "end")
        .attr("transform", null)
        .text(function (d) {
          return d.disp;
        })
        .filter(function (d) {
          return d.x < width / 2;
        })
        .attr("x", 6 + sankey.nodeWidth())
        .attr("text-anchor", "start");
    }

    function drawLink(data) {
      var group = graph.selectAll('g#normal').data([0]);
      group.enter().insert("g", ":first-child").attr('id', 'normal');
      console.log('sankey.data', data)
      var link = group.selectAll('path.link').data(data);
      link.exit().remove();

      link.enter().append("path")
        .attr("class", "link")
        .on("mouseover", funcMouseover)
        .on("mouseout", funcMouseout)
        .on('mousemove', funcMousemove)
        .on('dblclick', funcTooltipToggle);
        // .append("title");
      console.log('sankey.link()', link)
      link
        .attr("d", sankey.link())
        .style("stroke-width", function (d) {
          // return Math.max(1, d.dy);
          return 3
        })
        .sort(function (a, b) {
          return b.dy - a.dy;
        });

      // link.select('title')
      //   .text(function (d) {
      //     var text = formatNumber(d.value) + '\t' +
      //       d.source.disp + " → " + d.target.disp;
      //     return text;
      //   });
    }

    function drawDLink(data) {
      return graph.insert("g", ":first-child")
        .attr('id', 'highlight')
        .selectAll('path')
        .data(data)
        .enter()
        .append("path")
          .attr("class", "link highlight")
          .attr("d", sankey.link())
          .style("stroke-width", function (d) {
            return 10
            return Math.max(1, d.dy);
          })
          .sort(function (a, b) {
            return b.dy - a.dy;
          });
    }

    function funcMouseover(d) {
      sankey.dflows(d.flows);
      drawDLink(sankey.dlinks());
      updateTooltip(d);
      tooltipContainer.style('display', 'block');
    }
    function funcMouseout() {
      graph.selectAll("g#highlight").remove();
      tooltipContainer.style('display', 'none');
    }
    function funcMousemove() {
      tooltipContainer
        .style('top', d3.event.clientY + 'px')
        .style('left', d3.event.clientX + 'px');
    }
    function funcTooltipToggle(d){
      tooltipEnable = !tooltipEnable;
      updateTooltip(d);
    }

    ///////////////////////
    //// Tooltips

    function colorDot(d){
      return '<span style="background-color:'+ d.color +'"></span>';
    }

    sankey.nodes().forEach(function(n){
      n.tooltip = {
        name: colorDot(n) + n.disp,
        value: formatNumber(n.value),
        head: true,
      };
    });
    sankey.links().forEach(function(l){
      l.tooltip = {
        name: colorDot(l.source) + l.source.disp +
          " → " + colorDot(l.target) + l.target.disp,
        value: formatNumber(l.value),
        head: true,
      };

    });
    sankey.flows().forEach(function(f){
      var name = '';
      f.thru.forEach(function (n, ind) {
        if (ind !== 0) name += ' → ';
        name += colorDot(n) + n.disp;
      });
      f.tooltip = {
        name: name,
        value: formatNumber(f.value),
      };
    });

    //param d: data, could be node or link
    function updateTooltip(d){
      console.log('updateTooltip', d)
      tooltips = [d.tooltip];
      if (tooltipEnable){
        d.flows.forEach(function(f){
          tooltips.push(f.tooltip);
        });
      }

      //no need to use D3
      tbody.selectAll('*').remove();
      tooltips.forEach(function(tip){
        var tr = tbody.append('tr');
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
  };
};
