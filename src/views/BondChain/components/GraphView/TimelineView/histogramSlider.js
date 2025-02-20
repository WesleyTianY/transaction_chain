import * as d3 from 'd3'

export default function _histogramSlider(histogram, customOptions) {
  const defaultOptions = {
    'w': 760,
    'h': 150,
    'margin': {
      top: 20,
      bottom: 20,
      left: 20,
      right: 20
    },
    bucketSize: 1,
    defaultRange: [0, 100],
    format: d3.format('.3s')
  }

  const [min, max] = d3.extent(Object.keys(histogram).map(d => +d))
  const range = [min, max + 1]

  // Set width and height of svg
  // eslint-disable-next-line
  const { w, h, margin, defaultRange, bucketSize, format } = {...defaultOptions, ...customOptions}

  // Dimensions of slider bar
  const width = w - margin.left - margin.right
  const height = h - margin.top - margin.bottom

  // Create x scale
  const x = d3.scaleLinear()
    .domain(range)
    .range([0, width])
  const y = d3.scaleLinear()
    .domain([0, d3.max(Object.values(histogram))])
    .range([0, height])

  // Create svg and translated g
  const svg = d3.create('svg').attr('width', w).attr('height', h)
  const g = svg.append('g').attr('transform', `translate(${margin.left}, ${margin.top})`)

  // Draw histogram values
  g.append('g').selectAll('rect')
    .data(d3.range(range[0], range[1] + 1))
    .enter()
    .append('rect')
    .attr('x', d => x(d))
    .attr('y', d => height - y(histogram[d] || 0))
    .attr('width', width / (range[1] - range[0]))
    .attr('height', d => y(histogram[d] || 0))
    .style('fill', '#555')

  // Draw background lines
  g.append('g').selectAll('line')
    .data(d3.range(range[0], range[1] + 1))
    .enter()
    .append('line')
    .attr('x1', d => x(d))
    .attr('x2', d => x(d))
    .attr('y1', 0)
    .attr('y2', height)
    .style('stroke', '#ccc')

  // Labels
  g.append('text')
    .attr('id', 'label-min')
    .attr('x', -2)
    .attr('y', height + 15)
    .text(min)

  g.append('text')
    .attr('id', 'label-max')
    .attr('x', -2)
    .attr('y', -5)
    .text(max)

  g.append('text')
    .attr('id', 'labelleft')
    .attr('x', 0)
    .attr('y', height + 15)

  g.append('text')
    .attr('id', 'labelright')
    .attr('x', 0)
    .attr('y', height + 5)

  // Define brush
  const brush = d3.brushX()
    .extent([[0, 0], [width, height]])
    .on('brush', function() {
      const s = d3.event.selection
      g.select('#labelleft').attr('x', s[0]).text(format(Math.round(x.invert(s[0])) * bucketSize))
      g.select('#labelright').attr('x', s[1]).text(format((Math.round(x.invert(s[1])) - 1) * bucketSize))
    })

  // Append brush to g
  const gBrush = g.append('g')
    .attr('class', 'brush')
    .call(brush)

  // Select default range
  gBrush.call(brush.move, defaultRange
    .map(d => width * (d / 100))
    .map(x.invert)
    .map(Math.round)
    .map(x))

  return svg.node()
}
