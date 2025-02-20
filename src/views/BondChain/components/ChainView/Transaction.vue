<template>
  <div>
    <svg ref="chart" :width="width" :height="height" />
  </div>
</template>
<script>
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
// import { BCard, BIcon, BButton, BNavbar, BCardHeader, BCardBody, BDropdown, BDropdownItem, BIconGear, BDropdownGroup, BFormTags, BInputGroup, BInputGroupText, BFormInput, BButtonGroup, BButtonToolbar, BIconArrowUp, BIconArrowDown  } from 'bootstrap-vue'
import * as d3 from 'd3'
import axios from 'axios'
export default {
  components: {

  },
  data() {
    return {
      width: 775,
      height: 705
    }
  },
  mounted() {
    // this.getDataAndDraw()
  },
  methods: {
    async getDataAndDraw() {
      try {
        const response = await axios.get('http://localhost:5003/api/the_transaction_chains_data')
        console.log('response', response)
        const svg = d3.select(this.$refs.chart)
        this.drawChart(svg, response.data)
      } catch (error) {
        console.error('Error fetching data:', error)
      }
    },

    drawChart(svg, tangleLayout) {
      const options = {
        color: (b, i) => i % 2 === 0 ? 'blue' : 'blue'
      }

      // Draw links
      svg.selectAll('.link')
        .data(tangleLayout.bundles)
        .enter().append('g')
        .attr('class', 'link')
        .selectAll('path')
        .data(b => b.links)
        .enter().append('path')
        .attr('d', l => `M${l.xt} ${l.yt} L${l.xb} ${l.yt}`)
        .attr('stroke', (d, i) => options.color(tangleLayout.bundles[i], i))
        .attr('stroke-width', 2)

      // Draw nodes
      svg.selectAll('.node')
        .data(tangleLayout.nodes)
        .enter().append('circle')
        .attr('class', 'node')
        .attr('cx', d => d.xy_coordinates.x / 1.5)
        .attr('cy', d => (d.xy_coordinates.y + 50) / 1.5)
        .attr('r', 7)
        .attr('fill', d => `rgb(${d.color[0]}, ${d.color[1]}, ${d.color[2]})`)
        .attr('stroke-width', 2)

      // Draw node labels
      svg.selectAll('.label')
        .data(tangleLayout.nodes)
        .enter().append('text')
        .attr('class', 'label')
        .attr('x', d => d.xy_coordinates.x / 1.5)
        .attr('y', d => (d.xy_coordinates.y + 50) / 1.5)
        .attr('dy', '-1em')
        .attr('text-anchor', 'middle')
        // .text(d => d.name.slice(-2))
        .style('font-size', '8px')
    }
  }
}
</script>

<style>
/* 可以在这里添加样式 */
</style>
