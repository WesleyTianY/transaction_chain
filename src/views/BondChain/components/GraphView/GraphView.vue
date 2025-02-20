<template>
  <div>
    <b-card-header class="small-header" style="font-size:12px; height:25px;">
      <b-button variant="outline-secondary" style="font-size: 12px; float: right; margin-right:10px; padding: 0px 5px; height: 15px; display: flex; align-items: center;" @click="updateLassoAction('add')">
        <i class="el-icon-plus"></i>
      </b-button>
      <b-button variant="outline-secondary" style="font-size: 12px; float: right; margin-right:10px; padding: 0px 5px; height: 15px; display: flex; align-items: center;" @click="updateLassoAction('remove')">
        <i class="el-icon-minus"></i>
      </b-button>
    </b-card-header>
    <b-card-body class="graph_body" style=" height: 1100px; padding: 0px 0px 0px 0px; border: 0.5px solid rgba(204, 204, 204, 0.2)">
      <HistogramSlider />
      <div id="graph" style="height: 1100px; width: 1050px;"></div>
      <!-- <svg :id="'globalGraphView'" style="height: 675px; width: 893px;" /> -->
    </b-card-body>
  </div>

</template>
<script setup>
/* eslint-disable */
import ForceGraph from "../../dist/force-graph.js";
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'vue-slider-component/theme/default.css'
import { BCard, BIcon, BButton, BNavbar, BCardHeader, BCardBody, BDropdown, BDropdownItem, BIconGear, BDropdownGroup, BFormTags, BInputGroup, BInputGroupText, BFormInput, BButtonGroup, BButtonToolbar, BIconArrowUp, BIconArrowDown  } from 'bootstrap-vue'
import * as axios from 'axios'
// import ElementContainerVue from "./UI/ElementContainer.vue";
// import { getData } from "./files/service.js";
const { format } = require('date-fns')
import store from '@/store'
import { mapState, mapGetters, mapActions } from 'vuex'
import HistogramSlider from './TimelineView/HistogramSlider.vue';
import {contextmenu} from "@atago0129/d3-v4-contextmenu"
import { fetchTransactionChains } from '../../../../api/transactionChain.js';
export default {
  name: 'GraphView',
  components: {
    BCard,
    BIcon,
    BIconArrowUp, 
    BIconArrowDown,
    BButton,
    BCardHeader,
    BCardBody,
    BNavbar,
    BDropdown,
    BDropdownGroup,
    BDropdownItem,
    BIconGear,
    BFormTags,
    BInputGroup,
    BInputGroupText,
    BFormInput,
    BButtonGroup,
    BButtonToolbar,
    HistogramSlider
  },
  props: [],
  data() {
    return {
      jsonData: false,
      force: null,
      transaction_chains: null,
      mouseX: 0,
      mouseY: 0,
      showMenu: false,
    }
  },
  methods: {
    // contextmenus() {
    //   // https://github.com/pipipi-pikachu/v-contextmenu-directive?tab=readme-ov-file
    //   return [
    //     {
    //       text: 'Split',
    //     },
    //     { divider: true },
    //     {
    //       text: 'Delete',
    //     },
    //   ]
    // },
    // 处理右键菜单项点击事件
    handleContextMenuItemClick(item) {
        // console.log('Clicked on', item.label, 'with data', item.data);
        // 根据点击的操作执行相应的逻辑
    },
    // 在 SVG 上显示右键菜单
    showContextMenu(x, y, items) {
      // 可以根据鼠标点击的位置动态调整菜单的位置
      // 在此简化为固定位置
      const menuX = x;
      const menuY = y;
      console.log('Clicked 79', items);
      // 创建一个 div 元素用于显示右键菜单
      const contextMenu = d3.select("#globalGraphView")
          .append("div")
          .attr("class", "context-menu")
          .style("position", "absolute")
          .style("left", menuX + "px")
          .style("top", menuY + "px");
      // console.log("contextMenu", contextMenu)
      // 添加菜单项
      contextMenu.selectAll("div")
          .data(items)
          .enter()
          .append("div")
          .text(d => d.label)
          .on("click", function(item) {
              // 处理菜单项点击事件
              handleContextMenuItemClick(item);
              // 隐藏右键菜单
              contextMenu.remove();
          });

      // 点击菜单外部时隐藏菜单
      d3.select("#globalGraphView")
          .on("click.contextmenu", function() {
              contextMenu.remove();
          });
    },
    split(node) {
      // 处理拆分节点的逻辑
      console.log('splitFunction', node)
    },
    highlightPath(highlightedLinksData) {
      // 假设你有一个现有的 SVG 元素的选择器，例如 '#svg-container'
      const svg = d3.select('#globalGraphView');

      // 创建一个新的 SVG 元素用于高亮路径
      const highlightedPath = svg.append("g")
          .attr("class", "highlighted-path");

      // 在新的 SVG 元素上绘制高亮的路径
      highlightedPath.selectAll("line")
          .data(highlightedLinksData) // 这里的数据是路径上的边的数组
          .enter()
          .append("line")
          .attr("stroke", "blue") // 设置高亮颜色
          .attr("stroke-opacity", 1)
          .attr("x1", function(d) { return d.source.x; }) // 设置起始节点的 x 坐标
          .attr("y1", function(d) { return d.source.y; }) // 设置起始节点的 y 坐标
          .attr("x2", function(d) { return d.target.x; }) // 设置结束节点的 x 坐标
          .attr("y2", function(d) { return d.target.y; }) // 设置结束节点的 y 坐标
    },
    drawGraphCanvas(transaction_chains){
        const links = transaction_chains.links
        const nodes = transaction_chains.nodes
        // Random tree
        const gData = {
          nodes: nodes,
          links: links
        };
        // const gData = {
        //   nodes: [...Array(N).keys()].map(i => ({
        //     id: i,
        //     profit: Math.random() * 10, // random profit between -50 and 50
        //     loss: Math.random() * 10,
        //     transactions_info: {
        //       buy_num: Math.floor(Math.random()),
        //       sell_num: Math.floor(Math.random())
        //     },
        //     position: Math.random()*10,
        //     transaction_num: Math.random()*10
        //   })),
        //   links: [...Array(N).keys()]
        //     .filter(id => id)
        //     .map(id => ({
        //       source: id,
        //       target: Math.round(Math.random() * (id-1))
        //     }))
        // };
        const maxProfit = Math.max(...gData.nodes.map(node => Math.abs(node.trader_stats.offset_profit)));
        const maxLoss = Math.max(...gData.nodes.map(node => Math.abs(node.trader_stats.offset_profit)));
        const maxTransactions = Math.max(...gData.nodes.map(node => Math.abs(node.trader_stats.offset_count)))
        const elem = document.getElementById('graph');
        const Graph = ForceGraph()(elem)
        .width(elem.offsetWidth)  // 设置宽度为 div 的宽度
        .height(elem.offsetHeight) // 设置高度为 div 的高度
        // (document.getElementById('globalGraphView'))
        .linkDirectionalParticles(2)
        .linkDirectionalParticleSpeed(0.01)
        .graphData(gData)
        .nodeRelSize(20)
        .d3Force('charge', d3.forceManyBody().strength(-200))
        .dagLevelDistance(199)
        .onNodeClick(node => {
          console.log(node)
          // Center/zoom on node
          // Graph.centerAt(node.x, node.y, 1000);
          // Graph.zoom(2, 200);
        })
        // .onNodeRightClick()
        .minZoom(0.3)
        .maxZoom(0.8)
        .nodeCanvasObject((node, ctx, globalScale) => {

          const drawSolidCircle = (ctx, x, y, radius, color) => {
            ctx.beginPath();
            ctx.arc(x, y, radius, 0, 2 * Math.PI);
            ctx.fillStyle = color;
            ctx.fill();
            ctx.strokeStyle = "white";
            ctx.lineWidth = 1 / globalScale;
            ctx.stroke();
          };

          const drawRing = (ctx, x, y, innerRadius, outerRadius, startAngle, endAngle, color) => {
            const arcGenerator = d3.arc()
              .innerRadius(innerRadius)
              .outerRadius(outerRadius)
              .startAngle(startAngle)
              .endAngle(endAngle);

            const path = new Path2D(arcGenerator());
            ctx.fillStyle = color;
            ctx.fill(path);
            ctx.strokeStyle = "white";
            ctx.lineWidth = 1 / globalScale;
            ctx.stroke(path);
          };

          // Move the context to the node position
          ctx.save();
          ctx.translate(node.x, node.y);

          // Parameters for the arcs
          const profitPercentage = node.trader_stats.profit_percentage;
          const lossPercentage = node.trader_stats.profit_percentage;
          const startAngle = 0;
          // Draw inner ring left part
          // TODO: 
          // 1. Determine the upper and lower bound of the profit and loss
          // 2. Calculate the percentage of the profit and loss in the inner ring
          // 3. Draw the inner ring, profit is the right part of the inner ring, loss is the left part of the inner ring
          // 4. right part of the inner ring: startAngle = 0, endAngle = profitPercentage * 100 * (Math.PI / 180)
          // 5. left part of the inner ring: startAngle = - lossPercentage * 100 * (Math.PI / 180), endAngle = 0
          // 6. profitPercentage = node.profit / Max(node.profit)
          // Draw solid circle in the middle
          const solidCircleRadius = Math.sqrt(node.trader_stats.offset_volume*100)/Math.PI;
          drawSolidCircle(ctx, 0, 0, solidCircleRadius, "steelblue");

          // Draw inner ring left part (loss)
          const innerRingInnerRadius = solidCircleRadius;
          const innerRingOuterRadius = innerRingInnerRadius + 10;

          const innerRingLossStartAngle = -lossPercentage * (1 * Math.PI);
          const innerRingLossEndAngle = 0;
          drawRing(ctx, 0, 0, innerRingInnerRadius, innerRingOuterRadius, innerRingLossStartAngle, innerRingLossEndAngle, "hsl(0, 60%, 60%)");

          // Draw inner ring right part (profit)
          const innerRingProfitStartAngle = 0;
          const innerRingProfitEndAngle = profitPercentage * (1 * Math.PI);
          drawRing(ctx, 0, 0, innerRingInnerRadius, innerRingOuterRadius, innerRingProfitStartAngle, innerRingProfitEndAngle, "hsl(120, 60%, 60%)");

          // Draw outer ring
          const transaction_num_value = node.trader_stats.offset_count / maxTransactions * 10
          const outerRingInnerRadius = innerRingOuterRadius;
          const outerRingOuterRadius = outerRingInnerRadius + transaction_num_value;
          drawRing(ctx, 0, 0, outerRingInnerRadius, outerRingOuterRadius, 0, 360, "hsl(210, 90%, 80%)");

          ctx.restore();
        });
    },
    drawGraph(transaction_chains) {
        const links = transaction_chains.links
        const nodes = transaction_chains.nodes

        const width = 1063
        const height = 900
        // Create a simulation with several forces.
        const simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(links).id(d => d.id))
            .force("charge", d3.forceManyBody())
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force('x', d3.forceX().strength(0.015))
            .force('y', d3.forceY().strength(0.015))
            .on('tick', ticked)
        const maxOffsetVolume = d3.max(nodes, d => d.trader_stats.offset_volume)
        const scaleFactor = maxOffsetVolume / 20
        // Set the position attributes of links and nodes each time the simulation ticks.
        function ticked() {
          link
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y)
          node
            .attr('transform', d => `translate(${d.x},${d.y})`)
        }
        // function showContextMenu(x, y, items) {
        //   // 可以根据鼠标点击的位置动态调整菜单的位置
        //   // 在此简化为固定位置
        //   const menuX = x;
        //   const menuY = y;
        //   console.log('Clicked 79', items);
        //   // 创建一个 div 元素用于显示右键菜单
        //   const contextMenu = d3.select("#globalGraphView").append("g")
        //     .append("div")
        //     .attr("class", "context-menu")
        //     .style("position", "fixed") // 使用固定定位
        //     .style("left", x + "px")
        //     .style("top", y + "px");
        //   // contextMenu.append("text")
        //   //     .attr("id", "node-label")
        //   //     .attr("x", x)
        //   //     .attr("y", d => {
        //   //       return y
        //   //       })
        //   //     .text(items)
        //   //     .attr("fill", "black")
        //   //     .attr("font-size", "12px")
        //   //     .attr("font-family", "Arial")
        //   //     .attr("alignment-baseline", "middle")
        //   //     .attr("text-anchor", "middle");
        //   // console.log("contextMenu", contextMenu)
        //   // 添加菜单项
        //   contextMenu.selectAll("div")
        //       .data(items)
        //       .enter()
        //       .append("div")
        //       .text(d => d.label)
        //       .on("click", function(item) {
        //           // 处理菜单项点击事件
        //           handleContextMenuItemClick(item);
        //           // 隐藏右键菜单
        //           contextMenu.remove();
        //       });

        //   // 点击菜单外部时隐藏菜单
        //   d3.select("#globalGraphView")
        //       .on("click.contextmenu", function() {
        //           contextMenu.remove();
        //       });
        // }

        const svg = d3.select("#globalGraphView")
            .attr("width", width)
            .attr("height", height)
            .attr("viewBox", [0, 0, width, height])
            .attr("style", "max-width: 100%; height: auto;")
        var view = d3.select("#globalGraphView")
          .attr("class", "graphCon");
        // Add a line for each link, and a circle for each node.
        const link = svg.append("g")
            .attr("stroke", "#999")
            .attr("stroke-opacity", 0.6)
          .selectAll()
          .data(links)
          .join("line")

        const node = svg.append('g')
            .attr("stroke", "#fff")
            .attr("stroke-width", 1.5)
            .attr("stroke-linecap", "round")
            .attr("stroke-linejoin", "round")
          .selectAll("g")
          .data(nodes)
          .join("g")

        node.append("path")
            .attr("d", d => {
                const profit_percentage = d.trader_stats.profit_percentage / 100; // 从节点数据中获取Variance属性
                // 20 的值已经就是最大了，可以根据实际情况调整
                const radius = d.trader_stats.offset_volume / scaleFactor; // 甜甜圈的半径
                // const radius = 5; // 甜甜圈的半径
                const startAngle = 0; // 开始角度
                const endAngle = Math.PI * 2 * profit_percentage; // 结束角度，根据Variance来控制

                // 使用D3的arc生成器创建甜甜圈的路径
                const arcGenerator = d3.arc()
                    .innerRadius(radius - 10) // 内半径
                    .outerRadius(radius + 10) // 外半径
                    .startAngle(startAngle)
                    .endAngle(endAngle);

                return arcGenerator();
            })
            .attr("fill", d => d.trader_stats.profit_percentage >= 0 ? "hsl(0, 70%, 70%)" : "hsl(120, 70%, 40%)") // 根据正负设置填充颜色
            .attr("stroke", "white"); // 设置边框颜色
        node.append("path")
            .attr("d", d => {
                const offset_count = d.trader_stats.offset_count // 从节点数据中获取Variance属性
                // 20 的值已经就是最大了，可以根据实际情况调整
                const radius = d.trader_stats.offset_volume / scaleFactor; // 甜甜圈的半径
                // const radius = 5; // 甜甜圈的半径
                const startAngle = 0; // 开始角度
                const endAngle = Math.PI * 2 // 结束角度，根据Variance来控制

                // 使用D3的arc生成器创建甜甜圈的路径
                const arcGenerator = d3.arc()
                    .innerRadius(radius + 10 - offset_count) // 内半径
                    .outerRadius(radius + 10 + offset_count) // 外半径
                    .startAngle(startAngle)
                    .endAngle(endAngle);

                return arcGenerator();
            })
            .attr("fill", "hsl(210, 90%, 80%)") // 根据正负设置填充颜色
            .attr("stroke", "white"); // 设置边框颜色

        node.append("circle")
            .attr("r", function(d) {
              return d.trader_stats.offset_volume / scaleFactor
              })
            // .attr("fill", "steelblue")
            .attr("fill", function(d) {
                // 如果是做市商，涂色为紫色，否则为蓝色
                return d.statistics.is_market_maker ? "purple" : "steelblue";
            })
        node.on("mouseover", mouseover)
        .on("mouseout", mouseout)
        .on("click", function(d, p) {
          // console.log(p);
          node.each(function(d) {
            d3.select(this).style("opacity", 0.8).attr("stroke", "white");
          })
          d3.select(this).style("opacity", 1).attr("stroke", "black");

          d3.selectAll(".row text").classed("active", function(d, i) { return i == p; });
          d3.selectAll(".column text").classed("active", function(d, i) { return i == p; });
          // d3.selectAll(".row")
          //   .each(function(d, i) {
          //     if (i == p) {
          //       d3.select(this).selectAll("rect").style("fill", "red")//.style("stroke-opacity", 1);
          //     } else {
          //       d3.select(this).selectAll("rect")
          //       .each(function(d) {
          //         if (d.x == p) {
          //           d3.select(this).style("fill", "red")
          //         } else {
          //           d3.select(this).style("fill", "black")
          //         }
          //       })
          //     }
          //   })
        })

        node.on("contextmenu", function(event, d) {
            d3.event.preventDefault()
            // console.log("右键点击的点坐标：", event);
            // 获取右键单击的节点 ID
            const nodeId = event.id;
            const mouseX = event.x; // 鼠标点击的X坐标
            const mouseY = event.y; // 鼠标点击的Y坐标
            // console.log("节点坐标", mouseX, mouseY);
            // 构造右键菜单的选项
            const contextMenuItems = [
                { label: 'Option 1', action: 'option1', data: mouseX },
                { label: 'Option 2', action: 'option2', data: mouseY },
                // Add more options as needed
            ];
            showContextMenu(mouseX, mouseY, contextMenuItems)
            // 触发 Vuex action，并传递节点 ID 作为参数
            store.dispatch('TransactionChain/handleRightClick', nodeId);
        });
        function mouseover(node_info, d) {
            // 构造包含图和当前悬浮节点数据的对象
            // 在悬浮时显示节点 ID 的文本
            d3.select(this).style("opacity", 1).attr("stroke", "black")
            const topLayer = d3.select("#globalGraphView").append("g")
            // 获取鼠标事件的位置
            const x = node_info.x
            const y = node_info.y
            // console.log("node_info:", node_info)
            // 添加文本元素
            topLayer.append("text")
                .attr("id", "node-label")
                .attr("x", x)
                .attr("y", d => {
                  return y
                  })
                .text(d.id)
                .attr("fill", "black")
                .attr("font-size", "12px")
                .attr("font-family", "Arial")
                .attr("alignment-baseline", "middle")
                .attr("text-anchor", "middle");
            const dataToSend = {
                graph: transaction_chains,
                hoveredNode: node_info["id"]
            };
            // console.log("mouseover",  dataToSend);
            // 发起网络请求将数据发送到后端
            fetch('http://localhost:5003/api/process_hovered_node', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(dataToSend)
            })
            .then(response => response.json())
            .then(data => {
                // 处理从后端返回的数据
                // console.log('处理后端返回的数据：', data);
                // 在这里更新图的状态或执行其他操作
                // node.data(transaction_chains.nodes);
                // link.data(transaction_chains.links);

                // simulation.nodes(transaction_chains.nodes);
                // simulation.force("link").links(transaction_chains.links);
            })
            .catch(error => {
                console.error('发生错误：', error);
            });
        }
        function mouseout() {
            // simulation.alpha(0.001).restart();
            d3.select("#top-layer").select("#node-label").remove();
            d3.select("#top-layer").select("#node-label-bg").remove();
            d3.select(this).style("opacity", 0.8).attr("stroke", "white");
        }
        // node.append("title")
            // .text(d => d.id)

        // // Add a drag behavior.
        node.call(d3.drag()
              .on("start", dragstarted)
              .on("drag", dragged)
              .on("end", dragended))


        // Reheat the simulation when drag starts, and fix the subject position.
        function dragstarted() {
          if (!d3.event.active) simulation.alphaTarget(0.3).restart();
          d3.event.subject.fx = d3.event.subject.x;
          d3.event.subject.fy = d3.event.subject.y;
        }

        // Update the subject (dragged node) position during drag.
        function dragged() {
          d3.event.subject.fx = d3.event.x;
          d3.event.subject.fy = d3.event.y;
        }

        // Restore the target alpha so the simulation cools after dragging ends.
        // Unfix the subject position now that it’s no longer being dragged.
        function dragended() {
          if (!d3.event.active) simulation.alphaTarget(0)
          d3.event.subject.fx = null; // 清除固定位置
          d3.event.subject.fy = null; // 清除固定位置
        }

        // 生成一个包含对应连边的连边列表
        const shortestPathEdges = [];
        for (let i = 0; i < this.shortestPath.length - 1; i++) {
          const sourceNode = this.shortestPath[i];
          const targetNode = this.shortestPath[i + 1];
          // 遍历连边列表，根据节点列表来筛选出对应的连边
          shortestPathEdges.push([sourceNode, targetNode])
        }
        // console.log('selectedLine342', shortestPathEdges);

        const selectedElements = link._groups[0];
        selectedElements.forEach(element => {
          // 对每个选中的元素进行操作
          const data = element.__data__
          if (shortestPathEdges.some(edge => edge[0].id === data.source.id && edge[1].id === data.target.id)) {
            // console.log('selectedLine350', data);
            element.setAttribute("stroke", 'red');
          }
          else if (shortestPathEdges.some(edge => edge[1].id === data.source.id && edge[0].id === data.target.id)) {
            // console.log('selectedLine (reverse)', data.source.id, data.target.id);
            // 如果包含，设置元素的 stroke 为另一种颜色，例如蓝色
            element.setAttribute("stroke", 'red');
          }
          // console.log('selectedLine', data.source.id, data.target.id)
        });

        // function zoomed() {
        //   var transform = d3.event.transform;
        //   view.attr('transform',transform); 
        // }
        // //初始化缩放方法
        // var zoom = d3.zoom()
        // .scaleExtent([0.1, 10]).on("zoom", zoomed);
        // //画布开始缩放
        // svg.call(zoom)
        // .on("dblclick.zoom", () => {}); //禁止双击放大
    },
    // Define a method to redraw the graph with data from Vuex
    async getDataAndDraw(canvas) {
      try {
        const response = await fetchTransactionChains('34rr')
        console.log("chain response: " + response)
        console.log("chain : " + response)
        const transaction_chains = response.data;
        // const n = transaction_chains.nodes.length;
        console.log('transaction_chains', transaction_chains)
        // 在这里对数据进行修改
        // transaction_chains.nodes.forEach(function(d, i) {
        //   const width = 10;
        //   d.x = d.y = 10 + width / n * i;
        // });
        // console.log('transaction_chains', transaction_chains)

        // Dispatch action to update Vuex store
        // store.dispatch('TransactionChain/initializeGraph', transaction_chains)
        // store.dispatch('TransactionChain/findShortestPath', { start: '申港证券股份刘俊骥', end: '方正证券股份崔伟' })
        // store.dispatch('TransactionChain/updateTransactionChains', transaction_chains)
        //   .then(() => {
        //     console.log("action", ' 完成')
        //   })
        //   .catch((error) => {
        //     console.error('action', '出错', error)
        //   })
        // 然后调用绘制图形的函数来使用修改后的数据进行绘制
        
        // this.drawGraph(transaction_chains);
        this.drawGraphCanvas(transaction_chains)
        // this.highlightPath(this.shortestPath)
        } catch (error) {
          console.error('Error fetching data:', error);
        }
    },
    handleUserInteraction(data) {
      // Assume user interaction results in modified data
      const modifiedData = data // Compute modified data

      // Dispatch action to update the modified data in Vuex store
      this.$store.dispatch('TransactionChain/updateTransactionChains', modifiedData)
        .then(() => {
          // Data has been updated in Vuex, proceed to redraw the graph
          this.drawGraph();
        })
        .catch(error => {
          console.error('Error updating data in Vuex:', error);
        })
    },
  },
  created() {

  },
  mounted() {
    this.getDataAndDraw()
    const response = fetchTransactionChains('34rr')
    console.log("chain response: " + response)
  },
  watch: {

  },
  computed: {
    transactionChains() {
      return store.state.transactionChains;
    },
    shortestPath() {
      // console.log('shortestPath588', store.state.shortestPath)
      return store.state.shortestPath; // 通过 Vuex 获取最短路径信息
    },
    ...mapState({
      shortestPath: state => state.TransactionChain.shortestPath
    })
    // ...mapGetters('TransactionChain', [
    //   setTransactionChains

    //   ])
  },

}
</script>
<style>
.large-header{
    padding: 5px 5px 5px 10px;
    /* height: 5px; */
    font-size: 12px
}

.small-header{
    padding: 5px 5px 0px 20px;
    height: 33px
}

.menu {
  position: absolute;
  background-color: white;
  border: 1px solid #ccc;
  width: 150px;
  padding: 8px;
  z-index: 999;
}

.menu-item {
  cursor: pointer;
  padding: 4px 0;
}

/* .context-menu {
  display: none;
  position: fixed;
  background-color: #f9f9f9;
  border: 1px solid #ccc;
  padding: 5px 10px;
  z-index: 1000;
} */
</style>
