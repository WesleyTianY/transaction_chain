<template>
  <svg ref="timeLineView" :style="{ height: '100px', width: '760px', border: '0.5px solid rgba(204, 204, 204, 0.2)' }" />
</template>

<script>
// import * as d3 from 'd3'
import _histogramSlider from './histogramSlider.js'

export default {
  mounted() {
    // 获取SVG元素的引用
    const svgElement = this.$refs.timeLineView
    const histogramSlider = _histogramSlider({
      1: 12,
      2: 18,
      8: 14,
      9: 2,
      12: 22,
      15: 8,
      22: 3,
      26: 3,
      30: 6
    }, { h: 100, defaultRange: [25, 75], bucketSize: 10 })
    // 将创建的直方图滑块添加到SVG元素中
    svgElement.appendChild(histogramSlider)
  },
  methods: {
    // 定义样式
    // getStyle() {
    //   return `
    //     svg {
    //       font-family: -apple-system, system-ui, "avenir next", avenir, helvetica, "helvetica neue", ubuntu, roboto, noto, "segoe ui", arial, sans-serif
    //     }

    //     rect.overlay {
    //       stroke: #888;
    //     }

    //     rect.selection {
    //       stroke: none;
    //       fill: steelblue;
    //       fill-opacity: 0.4;
    //     }

    //     #labelleft, #labelright, #label-max, #label-min {
    //       font-size: 12px;
    //     }

    //     #labelleft, #labelright {
    //       dominant-baseline: hanging;
    //     }

    //     #label-min, #label-max {
    //       dominant-baseline: central;
    //       text-anchor: end;
    //     }

    //     #labelleft {
    //       text-anchor: end;
    //     }

    //     #labelright {
    //       text-anchor: start;
    //     }
    //   `
    // }
  }
}
</script>
