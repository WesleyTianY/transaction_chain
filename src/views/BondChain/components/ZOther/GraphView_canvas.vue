<template>
  <div>
    <b-card-header class="small-header" style="font-size:12px; height:25px;">
    </b-card-header>
    <!-- <div v-contextmenu="contextmenus" style="font-size:12px; height:125px;"></div> -->
    <b-card-body class="graph_body" style="overflow: scroll; height: 775px; padding: 5px 0px 5px 0px">
      <svg :id="'globalGraphView'" v-contextmenu="contextmenus" style="height: 770px; width: 1180px;" />
      <!-- <ElementContainerVue title="node-link"> -->
      <!-- <div ref="canvasContainer"></div> -->
      <!-- </ElementContainerVue> -->
    </b-card-body>
  </div>

</template>
<script setup>
/* eslint-disable */
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'vue-slider-component/theme/default.css'
import { BCard, BIcon, BButton, BNavbar, BCardHeader, BCardBody, BDropdown, BDropdownItem, BIconGear, BDropdownGroup, BFormTags, BInputGroup, BInputGroupText, BFormInput, BButtonGroup, BButtonToolbar, BIconArrowUp, BIconArrowDown  } from 'bootstrap-vue'
import * as axios from 'axios'
// import ElementContainerVue from "./UI/ElementContainer.vue";
// import { getData } from "./files/service.js";
const { format } = require('date-fns')
// import ForceGraph from './Force-graph/force-graph.js'; // 请根据实际路径调整
// import { directive, Contextmenu, ContextmenuItem } from "v-contextmenu"
// import "v-contextmenu/dist/themes/default.css";
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
  },
  props: [],
  data() {
    return {
      jsonData: false,
      force: null,
      transaction_chains: null
    }
  },
  methods: {
    initializeForce() {
      this.force = d3.layout.force()
        .size([width, height])
        .linkStrength(0.2)
        .linkDistance(100)
        .charge(-150);
    },
    readJSONData() {
      axios.get('server/static/chain_data/bond_2005496_2006_2402.json')
        .then(response => {
          this.jsonData = response.data;
        })
        .catch(error => {
          console.error('Error reading JSON file:', error);
        });
    },
    contextmenus() {
      // https://github.com/pipipi-pikachu/v-contextmenu-directive?tab=readme-ov-file
      return [
        {
          text: 'Split',
        },
        { divider: true },
        {
          text: 'Delete',
        },
      ]
    },
    createCanvas() {
      const dpi = window.devicePixelRatio;
      const width = 1500; // Width of the canvas
      const height = 700; // Height of the canvas
      const canvas = document.createElement("canvas");
      canvas.width = dpi * width * 1.2;
      canvas.height = dpi * height * 1.2;
      canvas.style.width = width + "px";
      canvas.style.maxWidth = "100%";
      canvas.style.height = "auto";
      this.$refs.canvasContainer.appendChild(canvas); // Append canvas to the container
      return canvas;
    },
    drawGraph(transaction_chains, canvas) {
      const color = d3.scaleOrdinal(d3.schemeCategory10);
      const links = transaction_chains.links;
      const nodes = transaction_chains.nodes;
      const width = 1500;
      const height = 800;
      const nodeRadius = 5
      const context = canvas.getContext("2d");
      const circles = []; // 保存节点信息的数组
      let transform = d3.zoomIdentity
      // 创建力导向图模拟器
      const simulation = d3.forceSimulation(nodes)
        .force("link", d3.forceLink(links).id(d => d.id))
        .force("charge", d3.forceManyBody().strength(-200))
        .force("center", d3.forceCenter(width / 2, height * 2 / 5))
        .force('x', d3.forceX().strength(0.07))
        .force('y', d3.forceY().strength(0.095))
        .on("tick", draw);
      console.log('transaction_chains', transaction_chains)
      function draw() {
          context.clearRect(0, 0, width, height);
          context.save();
          context.globalAlpha = 0.5;
          context.strokeStyle = "#999";
          context.beginPath();
          links.forEach(drawLink);
          context.stroke();
          context.restore();

          context.save();
          context.strokeStyle = "#fff";
          context.globalAlpha = 0.5;
          nodes.forEach(node => {
              context.beginPath();
              drawNode(node);
              // drawNode_pie(node);
              context.fillStyle = color(node.group);
              context.fill();
              context.stroke();
          });
          context.restore();
      }

      function drawLink(d) {
          context.moveTo(d.source.x, d.source.y);
          context.lineTo(d.target.x, d.target.y);
      }

      // function drawNode(node) {
      //     const radius = 7;
      //     const radiusSweet = 16; // 甜甜圈的半径
      //     const variance = node.normalized_statistics.Variance;

      //     // 绘制节点
      //     context.globalAlpha = 1;
      //     context.beginPath();
      //     context.arc(node.x, node.y, radius, 0, Math.PI * 2);
      //     // context.arc(node.x, node.y, radiusSweet, 0, Math.PI * 2 * variance);
      //     context.fillStyle = "#fff";
      //     context.fill();
      //     context.closePath(); // 关闭节点路径

      //     // 恢复全局透明度
      //     context.globalAlpha = 1;
      //     // 将节点信息存入 circles 数组
      //     circles.push({
      //         x: node.x,
      //         y: node.y,
      //         radius: radius,
      //         id: node.id,
      //     });
      // }

      // 绘制节点和甜甜圈
      function drawNode(node) {
          const radius = 7; // 节点半径
          const radiusSweet = 14; // 甜甜圈的半径
          const variance = node.normalized_statistics.Variance; // 节点的 Variance 值

          // 绘制甜甜圈
          context.globalAlpha = 0.5; // 设置甜甜圈的透明度
          context.beginPath();
          context.arc(node.x, node.y, Math.pow(variance, 0.01)*15, 0, Math.PI * 2);
          context.closePath();
          context.fillStyle = "#ff7f0e"; // 设置甜甜圈颜色
          context.fill(); // 填充甜甜圈

          // 绘制节点
          context.globalAlpha = 1;
          context.beginPath();
          context.arc(node.x, node.y, radius, 0, Math.PI * 2);
          context.closePath(); // 关闭节点路径
          context.fill(); // 填充节点
          // context.stroke(); // 描边节点
      }

      function handleClick(event) {
          const rect = canvas.getBoundingClientRect();
          const mouseX = event.clientX - rect.left;
          const mouseY = event.clientY - rect.top;
          const maxDistance = 20;
          const clickedNode = circles.find((circle) => {
              const dx = mouseX - circle.x;
              const dy = mouseY - circle.y;
              const distance = Math.sqrt(dx * dx + dy * dy);
              return distance < maxDistance;
          });
          if (clickedNode) {
              // console.log("Node clicked:", clickedNode.id);
          }
      }

      function findNode(nodes, x, y, radius) {
          const rSq = radius * radius;
          let i;
          for (i = nodes.length - 1; i >= 0; --i) {
            const node = nodes[i],
                  dx = x - node.x,
                  dy = y - node.y,
                  distSq = (dx * dx) + (dy * dy);
            if (distSq < rSq) {
              return node;
            }
          }
          // No node selected
          return undefined; 
        }
      function drag() {

        // Choose the circle that is closest to the pointer for dragging.
        function dragsubject(event) {
          let subject = null;
          let distance = maxDistance;
          for (const c of circles) {
            let d = Math.hypot(event.x - c.x, event.y - c.y);
            if (d < distance) {
              distance = d;
              subject = c;
            }
          }
          return subject;
        }

        // When starting a drag gesture, move the subject to the top and mark it as active.
        function dragstarted(event) {
          circles.splice(circles.indexOf(event.subject), 1);
          circles.push(event.subject);
          event.subject.active = true;
        }

        // When dragging, update the subject’s position.
        function dragged(event) {
          event.subject.x = Math.max(0, Math.min(width, event.x));
          event.subject.y = Math.max(0, Math.min(height, event.y));
        }

        // When ending a drag gesture, mark the subject as inactive again.
        function dragended(event) {
          event.subject.active = false;
        }

        return d3.drag()
            .subject(dragsubject)
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended);
      }
      // Add a drag behavior. The _subject_ identifies the closest node to the pointer,
      // conditional on the distance being less than 20 pixels.
      d3.select(canvas)
          .call(d3.drag()
            .subject(function() {
              const event = d3.event
              let subject = null;
              let distance = Infinity;
                for (const c of nodes) {
                  console.log(event)
                  console.log(c.x, c.y)
                  let d = Math.hypot(event.x - c.x, event.y - c.y);
                  if (d < distance) {
                    distance = d;
                    subject = c;
                  }
                }
              console.log("event.x, event.y:", event.x, event.y)

              console.log("subject:", subject)
              return subject; 
            })
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragEnded));

      function dragstarted(event) {
        if (!d3.event.active) {
          simulation.alphaTarget(0.3).restart();
        }
        d3.event.subject.fx = transform.invertX(d3.event.x);
        d3.event.subject.fy = transform.invertY(d3.event.y);
      }

      function dragged() {
        d3.event.subject.fx = transform.invertX(d3.event.x);
        d3.event.subject.fy = transform.invertY(d3.event.y);
      }

      function dragEnded() {
        if (!d3.event.active) {
          simulation.alphaTarget(0);
        }
        d3.event.subject.fx = null;
        d3.event.subject.fy = null;
      }

    },
    async getDataAndDraw(canvas) {
      try {
        const response = await axios.get('http://localhost:5003/api/get_transaction_chains_sample');
        const transaction_chains = response.data;
        const n = transaction_chains.nodes.length;

        // 在这里对数据进行修改
        transaction_chains.nodes.forEach(function(d, i) {
          const width = 10;
          d.x = d.y = 10 + width / n * i;
        });
        console.log('transaction_chains', transaction_chains)
        // 然后调用绘制图形的函数来使用修改后的数据进行绘制
        this.drawGraph(transaction_chains, canvas);
        } catch (error) {
          console.error('Error fetching data:', error);
        }
    }
  },
  created() {
    // axios.get('http://localhost:5003/api/get_transaction_chains/12')
    axios.get('http://localhost:5003/api/get_transaction_chains_sample')
      .then(response => {
        const transaction_chains = response.data
        // console.log("transaction_chains", transaction_chains)
        const color = d3.scaleOrdinal(d3.schemeCategory10)
        const links = transaction_chains.links
        const nodes = transaction_chains.nodes

        const width = 1180
        const height = 770

        const n = transaction_chains.nodes.length
        transaction_chains.nodes.forEach(function(d, i) {
          d.x = d.y =10+ width / n* i;
        })
        // Create a simulation with several forces.
        const simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(links).id(d => d.id))
            .force("charge", d3.forceManyBody())
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force('x', d3.forceX().strength(0.01))
            .force('y', d3.forceY().strength(0.01))
            .on('tick', ticked)

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

        const svg = d3.select("#globalGraphView")
            .attr("width", width)
            .attr("height", height)
            .attr("viewBox", [0, 0, width, height])
            .attr("style", "max-width: 100%; height: auto;")

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
            // .attr("fill", d => {
            //   // console.log("d.group:", d.group);
            //   return color(d.group);
            //         })


        node.append("path")
            .attr("d", d => {
                const radius = 8; // 甜甜圈的半径
                const variance = d.normalized_statistics.Variance; // 从节点数据中获取Variance属性
                const startAngle = 0; // 开始角度
                const endAngle = Math.PI * 2 * variance; // 结束角度，根据Variance来控制

                // 使用D3的arc生成器创建甜甜圈的路径
                const arcGenerator = d3.arc()
                    .innerRadius(radius - 7) // 内半径
                    .outerRadius(radius + 7) // 外半径
                    .startAngle(startAngle)
                    .endAngle(endAngle);

                return arcGenerator();
            })
            .attr("fill", "#ff7f0e") // 设置填充为透明，只显示边框
            .attr("stroke", "white"); // 设置边框颜色

        node.append("circle")
            .attr("r", 7)
            .attr("fill", "steelblue")

        node.on("mouseover", mouseover)
        .on("mouseout", mouseout)
        .on("click", function(d, p) {
          console.log(p);
          node.each(function(d) {
            d3.select(this).style("opacity", 0.8).attr("stroke", "white");
          })
          d3.select(this).style("opacity", 1).attr("stroke", "black");

          d3.selectAll(".row text").classed("active", function(d, i) { return i == p; });
          d3.selectAll(".column text").classed("active", function(d, i) { return i == p; });
          d3.selectAll(".row")
            .each(function(d, i) {
              if (i == p) {
                d3.select(this).selectAll("rect").style("fill", "red")//.style("stroke-opacity", 1);
              } else {
                d3.select(this).selectAll("rect")
                .each(function(d) {
                  if (d.x == p) {
                    d3.select(this).style("fill", "red")
                  } else {
                    d3.select(this).style("fill", "black")
                  }
                })
              }
            })
        })

        function mouseover(node_info, d) {
            // 构造包含图和当前悬浮节点数据的对象
            // 在悬浮时显示节点 ID 的文本
            d3.select(this).style("opacity", 1).attr("stroke", "black")
            const topLayer = d3.select("#globalGraphView").append("g")
            // 获取鼠标事件的位置
            const x = node_info.x
            const y = node_info.y
            // console.log("x", x, "y", y)
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
            // 添加节点名称文本背景框
            // const bbox = topLayer.select("#node-label").node().getBBox();
            // topLayer.insert("rect", "#node-label")
            //     .attr("id", "node-label-bg")
            //     .attr("x", bbox.x - 5)
            //     .attr("y", bbox.y - 3)
            //     .attr("width", bbox.width + 10)
            //     .attr("height", bbox.height + 6)
            //     .attr("fill", "white")
            //     .attr("stroke", "black")
            //     .attr("stroke-width", 0.5)
            //     .attr("rx", 4) // 圆角矩形
            //     .attr("ry", 4); // 圆角矩形
            const dataToSend = {
                graph: transaction_chains,
                hoveredNode: node_info["id"]
            };
            console.log("mouseover",  dataToSend);
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
                console.log('处理后端返回的数据：', data);
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

        function splitNode(d) {
            // 这里是根据自己的逻辑来计算分裂后的节点
            // 返回一个新节点的数组
            return [
                { id: d.id + "_1", x: d.x - 50, y: d.y + 50 },
                { id: d.id + "_2", x: d.x + 50, y: d.y + 50 }
            ];
        }
        // Reheat the simulation when drag starts, and fix the subject position.
        function dragstarted(event) {
          if (!d3.event.active) simulation.alphaTarget(0.3).restart();
          d3.event.subject.fx = d3.event.subject.x;
          d3.event.subject.fy = d3.event.subject.y;
        }

        // Update the subject (dragged node) position during drag.
        function dragged(event) {
          d3.event.subject.fx = d3.event.x;
          d3.event.subject.fy = d3.event.y;
        }

        // Restore the target alpha so the simulation cools after dragging ends.
        // Unfix the subject position now that it’s no longer being dragged.
        function dragended(event) {
          if (!d3.event.active) simulation.alphaTarget(0)
          d3.event.subject.fx = null; // 清除固定位置
          d3.event.subject.fy = null; // 清除固定位置
        }

      })
  },
  mounted() {
    const canvas = this.createCanvas();
    this.getDataAndDraw(canvas)
    // this.initGraph()
  },
  watch: {

  },
  computed: {
    // 计算属性用于筛选项目

  }
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
</style>
