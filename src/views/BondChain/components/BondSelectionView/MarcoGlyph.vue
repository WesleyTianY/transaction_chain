<template>
  <svg :id="'svg_marcoGlyph_' + bond_cd + '_' + end_date + '_' + duration_days" :end_date="end_date" :duration_days="duration_days" style="width: 100%; height: 40px" />
</template>

<script>
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import * as d3 from 'd3'
// const d3 = require('d3')
import Mock from 'mockjs'
const { format } = require('date-fns')
import MultiData from './MultiData'
import _ from 'lodash'
export default {
  // eslint-disable-next-line
  props: ['bond_cd', 'end_date', "duration_days"],
  data() {
    return {
    }
  },
  created() {

  },
  mounted() {
    // const dataPackage = this.dataPackageGeneration(this.bond_cd, this.end_date, this.duration_days)
    // this.drawMultiCharts(dataPackage, this.bond_cd, this.end_date, this.duration_days)
    // const dataPackage1 = this.fetchData()
    // console.log('dataPackage1', dataPackage1)
    this.dataPackages = this.fetchData()
  },

  methods: {
    dataPackageGeneration(bond_cd, date, duration_days) {
      class MultiData {
        constructor(bond_cd, date, duration_days) {
          const dataPackage = {}
          dataPackage['mktPrice'] = this.generateMarketPriceData(bond_cd, date, duration_days)
          dataPackage['transaction'] = this.generateTransactionData(bond_cd, date, duration_days)
          dataPackage['valuation'] = this.generateValuationData(bond_cd, date, duration_days)
          dataPackage['volume'] = this.generateMarketPriceData(bond_cd, date, duration_days)
          dataPackage['gradient'] = this.generateMarketPriceData(bond_cd, date, duration_days)
          this.dataPackage = dataPackage
        }
        generateMarketPriceData(bond_cd, date, duration_days) {
          const _MarketPriceList = []
          for (let offset = duration_days; offset >= 0; offset--) {
            var numMarketPrice = Mock.Random.integer(40, 60)
            for (let num = 1; num <= numMarketPrice; num++) {
              const _MarketPrice = {
                'bond_cd': bond_cd,
                'netValue': Mock.Random.float(90, 110, 2, 2), // Generate random float between 80 and 120 for 最新净价
                'tradeVolume': Mock.Random.integer(10, 1000), // Generate random integer between 100 and 1000 for 成交量
                'timeStamp': this._randomDateInRange(date, offset).toLocaleString()
              }
              _MarketPriceList.push(_MarketPrice)
            }
          }
          return _MarketPriceList
        }
        generateTransactionData(bond_cd, date, duration_days) {
          // 交易数据类似于行情数据，不过画图的时候有区别，并且数量更少
          const _TransactionList = []
          for (let offset = duration_days; offset >= 0; offset--) {
            var numTransactions = Mock.Random.integer(40, 60)
            for (let num = 1; num <= numTransactions; num++) {
              const _Transaction = {
                'bond_cd': bond_cd,
                'transactionId': Mock.Random.string('upper', 3, 4),
                'netPrice': Mock.Random.float(95, 105, 0, 2),
                'transactionVolume': Mock.Random.float(10, 400),
                'tradeResult': Mock.Random.boolean(),
                'timeStamp': this._randomDateInRange(date, offset).toLocaleString()
              }
              _TransactionList.push(_Transaction)
            }
          }
          return _TransactionList
        }
        generateValuationData(bond_cd, date, duration_days) {
          // 估值数据其实是一天就一个值
          const _ValuationDataList = []
          for (let offset = duration_days; offset > 0; offset--) {
            // get the offset date
            var offsetDate = new Date(date)
            offsetDate.setDate(offsetDate.getDate() - offset)
            const formattedDate = format(offsetDate, 'yyyy-MM-dd') // 格式化为只包含日期

            const _ValuationData = {
              'bond_cd': bond_cd,
              'valuationPrice': Mock.Random.float(98, 103, 2, 2),
              'profitRate': Mock.Random.float(0.02, 0.04, 2, 2),
              'recommendFlag': Mock.Random.boolean(),
              'timeStamp': formattedDate
            }
            _ValuationDataList.push(_ValuationData)
          }
          return _ValuationDataList
        }
        _randomDateInRange(date, offset) {
          var dateTime = new Date(date + ' 09:00:00')
          // 获取offset天的日期
          var offsetStartDate = new Date()
          var offsetEndDate = new Date()
          offsetStartDate.setTime(dateTime)
          offsetEndDate.setTime(dateTime)
          offsetStartDate.setDate(offsetStartDate.getDate() - offset)
          offsetEndDate.setDate(offsetEndDate.getDate() - offset)

          // 设置时间
          offsetStartDate.setHours(9, 30, 0, 0)
          offsetEndDate.setHours(15, 0, 0, 0)

          // 获取时间戳
          var offsetStartTimestamp = offsetStartDate.getTime()
          var offsetEndTimestamp = offsetEndDate.getTime()
          var randomOffsetTimestamp = Mock.Random.integer(offsetStartTimestamp, offsetEndTimestamp)

          return new Date(randomOffsetTimestamp)
        }
        generateGradient() {

        }
        volumeStatistic() {

        }
      }
      const multiData = new MultiData(bond_cd, date, duration_days)
      return multiData.dataPackage
    },

    drawMultiCharts(data, bond_cd, endDay, duration_days, vueComponent, theLimits) {
      // 一个对象将是1个bond多天的数据，多个feature
      // 所以需要考虑将多天的数据画出来，所以要拆分上下午
      // 定义 DayDataDrawer 类
      class MultiChart {
        constructor(data, bond_cd, endDay, duration_days, vueComponent, theLimits) {
          this.allData = data
          this.bond_cd = bond_cd
          this.endDay = endDay
          this.duration_days = duration_days
          this.margin = { top: 3, right: 3, bottom: 3, left: 3 }
          this.width = 297
          this.height = 40
          this.vueComponent = vueComponent // 保存 Vue 组件的上下文
          // console.log('theLimits 144:', theLimits)
          this.upper = theLimits[1]
          this.lower = theLimits[0]
          var chartContainer = d3.select('#svg_marcoGlyph_' + bond_cd + '_' + endDay + '_' + duration_days)
            .append('svg')
            .append('g')
            .attr('width', this.width)
            .attr('height', this.height)
            // .attr('transform', `translate(${this.margin.left}, ${this.margin.top})`)
          this.chartContainer = chartContainer
          // eslint-disable-next-line
          // var lassoContainer = this.chartContainer.append('svg')
          //   .attr('width', this.width)
          //   .attr('height', this.height)
          //   .attr('name', 'lassoContainer')
          // this.lassoContainer = lassoContainer
          var lineContainer = this.chartContainer.append('svg')
            .attr('width', this.width)
            .attr('height', this.height)
            .attr('name', 'lineContainer')
          this.lineContainer = lineContainer
          // var VolumeBarContainer = this.chartContainer.append('svg')
          //   .attr('width', this.width)
          //   .attr('height', this.height)
          //   .attr('name', 'VolumeBarContainer')
          // this.VolumeBarContainer = VolumeBarContainer
        }
        drawMultiDayData(dimension) {
          const singleFeaList = this.allData[dimension] // 获取多天数据
          // console.log('singleFeaList', dimension, singleFeaList)
          const sortedSingleFeaList = singleFeaList.sort((a, b) => new Date(a.timeStamp) - new Date(b.timeStamp))
          const groupedData = sortedSingleFeaList.reduce((groups, item) => {
            const date = item.timeStamp.substr(0, 10)
            if (!groups[date]) groups[date] = []
            groups[date].push(item)
            return groups
          }, {})
          // console.log('177 groupedData', groupedData)
          // 计算有多少天。得到多少个上午和下午，按照这个个数来划分offset，可能需要平移
          const groupCount = Object.keys(groupedData).length * 2
          Object.entries(groupedData).forEach(([theDate, singleDayDataList], index) => {
            // dayData 进行拆分 分别变为 dayData.morning与dayData.afternoon
            const xOffset_morning = 2 * index / groupCount * this.width/* 计算偏移 */
            const xOffset_afternoon = (2 * index + 1) / groupCount * this.width/* 计算偏移 */
            // console.log('data', singleDayDataList)
            // const morningData = this.dataFilter(singleDayDataList, theDate)
            // const afternoonData = this.dataFilter(singleDayDataList, theDate)
            const oneDayData_new = this.dataFilter(singleDayDataList, theDate)
            const oneDayData = _.cloneDeep(oneDayData_new)
            // console.log('oneDayData', oneDayData)
            const morningDataList = oneDayData[0].AM
            const afternoonDataList = oneDayData[0].PM
            const morningData = _.cloneDeep(morningDataList)
            const afternoonData = _.cloneDeep(afternoonDataList)
            // console.log('morningData', morningData)
            // console.log('afternoonData', afternoonData)
            // console.log('xOffset', xOffset_morning, xOffset_afternoon)
            // 基于早上和下午的数据进行画图，目标是定义好的svg上，画maket的图，就是画5个，所以输入是：
            // bond_cd、duration_days、endDay、morningData、afternoonData、dimension
            this.drawDayData(morningData, dimension, theDate, xOffset_morning, 'AM', groupCount)
            this.drawDayData(afternoonData, dimension, theDate, xOffset_afternoon, 'PM', groupCount)
          })
        }
        drawDayData(data, dimension, date, xOffset, time_Period, groupCount) {
        // 基于早上和下午的数据进行画图，目标是定义好的svg上，画maket的图，就是画5个，所以输入是：
        // bond_cd、duration_days、endDay、morningData、afternoonData、dimension
        // Draw data using the stored draw function
          var startTimePoint = false
          var endTimePoint = false
          if (time_Period === 'AM') {
            startTimePoint = this.offsetTime(date, 9, 30)
            endTimePoint = this.offsetTime(date, 11, 30)
          }
          if (time_Period === 'PM') {
            startTimePoint = this.offsetTime(date, 13, 30)
            endTimePoint = this.offsetTime(date, 15, 0)
          }
          switch (dimension) {
            case 'mktPrice':
              this.drawMktPriceLine(data, xOffset, startTimePoint, endTimePoint, groupCount)
              break
            case 'valuation':
              this.drawValuationLine(data, xOffset, startTimePoint, endTimePoint, groupCount)
              break
            case 'transaction':
              this.drawTrasactionScatter(data, xOffset, startTimePoint, endTimePoint, groupCount)
              break
            case 'volume':
              this.drawVolumeBar(data, xOffset, startTimePoint, endTimePoint, groupCount)
              break
            case 'gradient':
              this.drawGradTimeline(data, xOffset, startTimePoint, endTimePoint, groupCount)
              break
          }
        }
        formatDateToCustomString(dateString) {
          const originalDate = new Date(dateString)

          const year = originalDate.getFullYear()
          const month = (originalDate.getMonth() + 1).toString().padStart(2, '0')
          const day = originalDate.getDate().toString().padStart(2, '0')
          const hours = originalDate.getHours().toString().padStart(2, '0')
          const minutes = originalDate.getMinutes().toString().padStart(2, '0')
          const seconds = originalDate.getSeconds().toString().padStart(2, '0')

          const formattedDate = `${year}_${month}_${day}_${hours}_${minutes}_${seconds}`
          return formattedDate
        }
        formatDateToCustomDateString(dateString) {
          const originalDate = new Date(dateString)

          const year = originalDate.getFullYear()
          const month = (originalDate.getMonth() + 1).toString().padStart(2, '0')
          const day = originalDate.getDate().toString().padStart(2, '0')
          const hours = originalDate.getHours().toString().padStart(2, '0')
          const minutes = originalDate.getMinutes().toString().padStart(2, '0')
          const seconds = originalDate.getSeconds().toString().padStart(2, '0')

          const formattedDate = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
          return formattedDate
        }
        offsetTime(originalDateString, hoursOffset, minutesOffset) {
          const originalDate = new Date(originalDateString)
          const offsetMilliseconds = (hoursOffset * 3600 + minutesOffset * 60) * 1000
          const newTime = originalDate.getTime() + offsetMilliseconds
          const newDate = new Date(newTime)

          const year = newDate.getFullYear()
          const month = (newDate.getMonth() + 1).toString().padStart(2, '0')
          const day = newDate.getDate().toString().padStart(2, '0')
          const hours = newDate.getHours().toString().padStart(2, '0')
          const minutes = newDate.getMinutes().toString().padStart(2, '0')
          const seconds = newDate.getSeconds().toString().padStart(2, '0')

          const formattedDate = `${year}-${month}-${day}T${hours}:${minutes}:${seconds}.000Z`
          return formattedDate
        }
        drawMktPriceLine(data, xOffset, startTimePoint, endTimePoint, groupCount) {
          // 定义时间解析器
          // var parseTime = d3.timeParse('%Y/%m/%d %H:%M:%S')
          // data.forEach(function(d) { d.timeStamp = parseTime(d.timeStamp) })
          data.forEach(function(d) {
            const timeWithoutTimezone = d.timeStamp.slice(0, -6)
            d.timeStamp = timeWithoutTimezone
            d.timeStamp = new Date(d.timeStamp)
          })
          data.sort((a, b) => a.timeStamp - b.timeStamp)
          startTimePoint = this.formatDateToCustomDateString(startTimePoint)
          endTimePoint = this.formatDateToCustomDateString(endTimePoint)
          // const colors = ['#f7fbff', '#deebf7', '#c6dbef', '#9ecae1', '#6baed6', '#4292c6', '#2171b5', '#08519c', '#08306b']
          // eslint-disable-next-line
          const xScale = d3.scaleTime().range([0, this.width / groupCount])
            .domain([d3.min(data, d => d.timeStamp), d3.max(data, d => d.timeStamp)])
          const yScale = d3.scaleLinear().range([this.height, 0])
            .domain([d3.min(data, d => d.netValue), d3.max(data, d => d.netValue)])
          // eslint-disable-next-line
          const area = d3.area()
            .x((d) => xScale(d.timeStamp))
            .y0(yScale(0))
            .y1((d) => yScale(d.netValue))

          // Add a rectangular clipPath and the reference area.
          const defs = this.lineContainer.append('g')

          defs.append('path')
            .attr('transform', `translate(${xOffset}, 0)`)
            .style('stroke', d3.schemeRdYlBu[3][2])
            .style('stroke-width', 2)
            .attr('d', area(data))
            .attr('fill', d3.schemeRdYlBu[3][2])
            // .attr('fill', colors[4])
        }
        drawValuationLine(data, xOffset, startTimePeriod, endTimePeriod) {
          const rScale = d3.scaleLinear().domain([0, d3.max(data, (d) => d.transactionVolume)]).range([0, 10])
          this.chartContainer.selectAll('rect')
            .data(data)
            .enter()
            .append('rect')
            .attr('cx', (d, i) => i * 10)
            .attr('cy', (d, i) => this.height - 1 * d.netPrice)
            .attr('r', (d, i) => rScale(d.transactionVolume))
        }
        drawTrasactionScatter(data, xOffset, startTimePoint, endTimePoint, groupCount) {
          // 定义时间解析器
          // this.chartContainer.selectAll('circle').remove()
          // var parseTime = d3.timeParse('%Y/%m/%d %H:%M:%S')
          // data.forEach(function(d) { d.timeStamp = parseTime(d.timeStamp) })
          data.forEach(function(d) {
            const timeWithoutTimezone = d.timeStamp.slice(0, -6)
            d.timeStamp = timeWithoutTimezone
            d.timeStamp = new Date(d.timeStamp)
          })
          startTimePoint = this.formatDateToCustomDateString(startTimePoint)
          endTimePoint = this.formatDateToCustomDateString(endTimePoint)
          const xScale = d3.scaleTime().range([0, (this.width / groupCount)])
            // .domain([d3.min(data, d => d.timeStamp), d3.max(data, d => d.timeStamp)])
            // .domain([new Date(startTimePoint), new Date(endTimePoint)])
            .domain([d3.min(data, d => d.timeStamp), d3.max(data, d => d.timeStamp)])
          const yScale = d3.scaleLinear().range([this.height * 0.25, this.height * 0.95])
            .domain([d3.min(data, d => d.netPrice), d3.max(data, d => d.netPrice)])
          // const max = d3.max(data, d => Math.abs(d.transactionVolume))
          // const min = d3.min(data, d => Math.abs(d.transactionVolume))
          // const color = d3.scaleSequential().domain([max, min])
          //   .interpolator(d3.interpolateRdBu)
          // const color = d3.interpolateRdBu(0.31)
          // const color_add = d3.rgb(174, 219, 155)
          // const color_remove = d3.rgb(162, 162, 162)
          // const color_selected = d3.rgb(219, 76, 85)
          const color_default = d3.rgb(255, 210, 186)
          const rScale = d3.scaleLinear().range([1, 5]).domain([d3.min(data, d => d.transactionVolume), d3.max(data, d => d.transactionVolume)])
          this.lassoContainer.append('g')
            .attr('stroke', '#000')
            .attr('stroke-opacity', 0.2)
            .selectAll('circle')
            .data(data)
            .enter()
            .append('circle')
            .attr('cx', d => xScale(d.timeStamp))
            .attr('cy', d => this.height - yScale(d.netPrice))
            .attr('r', d => rScale(d.transactionVolume))
            .attr('fill', d => color_default)
            .attr('transform', `translate(${xOffset}, 0)`)
            .style('opacity', 0.6)
        }
        // highlightCircles() {
        //   // 获取 Vuex 中的 GlobalLassoData
        //   const globalLassoData = this.vueComponent.getGlobalLassoData
        //   const color_add = d3.rgb(174, 219, 155)
        //   const color_remove = d3.rgb(162, 162, 162)
        //   const color_selected = d3.rgb(219, 76, 85)
        //   const color_default = d3.rgb(255, 210, 186)
        //   if (globalLassoData !== undefined) {
        //     // 遍历数据点
        //     this.lassoContainer.selectAll('circle')
        //       .each(function(d) {
        //         const circle = d3.select(this)
        //         // 假设数据点有一个唯一的标识符，例如 id
        //         const pointId = d.transactionId // 假设 id 是数据点的标识符属性

        //         // 检查数据点是否在 GlobalLassoData 中
        //         const isSelected = globalLassoData.some(item => item.transactionId === pointId)

        //         // 根据 isSelected 的值来选择涂色
        //         if (isSelected) {
        //           circle.style('fill', color_selected)
        //         } else {
        //           circle.style('fill', color_default)
        //         }
        //       })
        //   }
        // }
        drawVolumeBar(data, xOffset, startTimePoint, endTimePoint, groupCount) {
          const timeGranularity = 10
          const groupedDataArray = this.bucketDataByMinute(data, timeGranularity)
          // 定义时间解析器
          data.forEach(function(d) {
            const timeWithoutTimezone = d.timeStamp.slice(0, -6)
            d.timeStamp = timeWithoutTimezone
            d.timeStamp = new Date(d.timeStamp)
          })
          startTimePoint = this.formatDateToCustomDateString(startTimePoint)
          endTimePoint = this.formatDateToCustomDateString(endTimePoint)

          // Calculate the sum of trade volumes for each group
          const sums = groupedDataArray.map(group => d3.sum(group, d => d.tradeVolume))
          // Find the maximum sum
          const maxSum = d3.max(sums)
          const xScale = d3.scaleTime().range([0, this.width / groupCount])
            .domain([d3.min(data, d => d.timeStamp), d3.max(data, d => d.timeStamp)])
            // .domain([startTimePoint, endTimePoint])
            // .domain([new Date(startTimePoint), new Date(endTimePoint)])
          const yScale = d3.scaleLinear().range([0, this.height * 0.1])
            .domain([0, maxSum])
          this.VolumeBarContainer.append('g').selectAll('rect')
            .data(groupedDataArray)
            .attr('class', 'volumeBar')
            .enter()
            .append('rect')
            // .style('stroke', d3.schemeSet2[1])
            .attr('x', d => xScale(d[0].timeStamp))
            .attr('y', d => 0.9 * this.height - yScale(d3.sum(d, d => d.tradeVolume)))
            .attr('height', d => yScale(d3.sum(d, d => d.tradeVolume)))
            .attr('width', this.width / groupCount / (150 / timeGranularity))
            .attr('fill', 'SteelBlue')
            .attr('transform', `translate(${xOffset}, 0)`)
            .on('mouseover', function() {
              // Update fill on mouseover
              d3.select(this)
                .attr('fill', 'Maroon')
            })
            .on('mouseout', function() {
              // Update fill on mouseout
              d3.select(this)
                .attr('fill', 'SteelBlue')
            })
        }
        bucketDataByMinute(data, minutes) {
          const groupedData = {}
          data.forEach(function(d) {
            const timeStamp = new Date(d.timeStamp)
            const bucketKey = Math.floor(timeStamp.getMinutes() / minutes) * minutes
            if (!groupedData[bucketKey]) {
              groupedData[bucketKey] = []
            }
            groupedData[bucketKey].push(d)
          })
          const groupDataArray = Object.values(groupedData)
          return groupDataArray
        }
        drawGradTimeline(data, xOffset, startTimePoint, endTimePoint, groupCount) {
          const timeGranularity = 10
          // eslint-disable-next-line
          const groupedDataArray = this.bucketDataByMinute(data, timeGranularity)
          // console.log('groupedDataArray:', groupedDataArray)
          // 定义时间解析器
          var parseTime = d3.timeParse('%Y/%m/%d %H:%M:%S')
          data.forEach(function(d) { d.timeStamp = parseTime(d.timeStamp) })
          startTimePoint = this.formatDateToCustomDateString(startTimePoint)
          endTimePoint = this.formatDateToCustomDateString(endTimePoint)

          // Calculate the sum of trade volumes for each group
          // const sums = groupedDataArray.map(group => d3.sum(group, d => d.tradeVolume))
          // Find the maximum sum
          // const maxSum = d3.max(sums)
          // console.log(dataByItems)
          // eslint-disable-next-line
          const xScale = d3.scaleTime().range([0, this.width])
            .domain([d3.min(data, d => d.timeStamp), d3.max(data, d => d.timeStamp)])
            // .domain([startTimePoint, endTimePoint])
            // .domain([new Date(startTimePoint), new Date(endTimePoint)])
          // eslint-disable-next-line
          // const yScale = d3.scaleLinear().range([0, this.height * 0.1])
            // .domain([0, maxSum])
          // eslint-disable-next-line
          /* eslint-disable */
          const parseTimenew = d3.timeParse('%Y-%m-%dT%H:%M:%S.%LZ')
          timelineData.forEach(function(d) {
            d.startDate = parseTimenew(d.startDate)
            d.endDate = parseTimenew(d.endDate)
            })
          this.chartContainer.append('g')
            .selectAll('rect')
            .data(timelineData)
            .enter()
            .append('rect')
            .attr('x', d => xScale(d.startDate))
            .attr('y', this.height - 10)
            .attr('width', d => xScale(d.endDate) - xScale(d.startDate))
            .attr('height', 10)
            .attr('fill', '#FFD325')
            .attr('rx', 4)
            .attr('stroke', 'white')
            .style('stroke-width', 2)
            .attr('fill', 'none')

          // console.log('timelineData', timelineData)

          // timelineInstance = timeline()
            // .size([400, 20])
            // .bandStart(function(d) {
            //   return new Date(d.startDate);
            // })
            // .bandEnd(function(d) {
            //   return new Date(d.endDate);
            // })
        }
        generateVirtualFeature(date, timePeriod, dimension) {
          const dimensionFeatures = {
            'transactionData': {
              timeStamp: 'timeStamp',
              netValue: null,
              tradeVolume: null
            },
            'valuationData': {
              timeStamp: 'timeStamp',
              netValue: null,
              tradeVolume: null,
              bond_cd: null,
              valuationPrice: null,
              profitRate: null,
              recommendFlag: null
            }
            // 添加其他维度的特征
          }
          const feature = dimensionFeatures[dimension]
          const virtualData = {}
          if (feature) {
            virtualData['timeStamp'] = date + timePeriod.timeStamp
            for (const prop in feature) {
              if (prop !== 'timeStamp') {
                virtualData[prop] = feature[prop]
              }
            }
          }
          return virtualData
        }
        // dataFilter(data, theDate, timePeriod, dimension) {
        //   // 输入的数据是一天的数据 多个维度
        //   const combinedData = []

        //   const startTime_AM = new Date(`${theDate} 09:00:00`)
        //   const endTime_AM = new Date(`${theDate} 11:30:00`)
        //   const startTime_PM = new Date(`${theDate} 13:30:00`)
        //   const endTime_PM = new Date(`${theDate} 16:00:00`)

        //   const sortedData = data.sort((a, b) => new Date(a.timeStamp) - new Date(b.timeStamp))
        //   const firstTimestamp = new Date(sortedData[0].timeStamp)
        //   const lastTimestamp = new Date(sortedData[sortedData.length - 1].timeStamp)

        //   const combinedGroup = []
        //   // 排序分组数据
        //   switch (timePeriod) {
        //     case 'AM':
        //       if (firstTimestamp < startTime_AM) {
        //         // const virtualFeature = this.generateVirtualFeature(theDate, startTime_AM, dimension)
        //         // combinedGroup.push(virtualFeature)
        //       }
        //       combinedGroup.push(...sortedData.filter(item => new Date(item.timeStamp) >= startTime_AM && new Date(item.timeStamp) <= endTime_AM))
        //       break
        //     case 'PM':
        //       if (firstTimestamp < startTime_PM) {
        //         // const virtualFeature = this.generateVirtualFeature(theDate, startTime_PM, dimension)
        //         // combinedGroup.push(virtualFeature)
        //       }
        //       combinedGroup.push(...sortedData.filter(item => new Date(item.timeStamp) >= startTime_PM && new Date(item.timeStamp) <= endTime_PM))
        //       break
        //   }

        //   if (lastTimestamp > endTime_PM) {
        //     const virtualFeature = this.generateVirtualFeature(theDate, endTime_PM, dimension)
        //     combinedGroup.push(virtualFeature)
        //   }
        //   combinedData.push(...combinedGroup)

        //   return combinedData
        // }
        dataFilter(data, theDate) {
          const combinedData = []
          if (!Array.isArray(data)) {
            // 如果 data 不是数组，你可以尝试将其转换为数组
            data = [data]
          }
          const splitTime = new Date(`${theDate} 12:00:00+08:00`)
          // console.log('splitTime', splitTime)
          const AMData = data.filter(item => new Date(item.timeStamp) < splitTime)
          const PMData = data.filter(item => new Date(item.timeStamp) >= splitTime)

          combinedData.push({ 'AM': AMData, 'PM': PMData })

          return combinedData
        }
      }
      const multiChart = new MultiChart(data, bond_cd, endDay, duration_days, this, theLimits)
      // multiChart.drawMultiDayData('transaction')
      multiChart.drawMultiDayData('mktPrice') // 在市场价格维度上绘制多天数据
      // multiChart.drawMultiDayData('volume')
      // multiChart.lassoFunction()
      // multiChart.drawMultiDayData('gradient') // 在估值维度上绘制多天数据
    },

    async fetchData() {
      function average_var(data) {
        const average = data.reduce((total, price) => total + price, 0) / data.length
        const variance = data.reduce((total, price) => total + Math.pow(price - average, 2), 0) / data.length
        return [average, variance]
      }
      function upperLowerLimits(statistic) {
        const average = statistic[0]
        const variance = statistic[1]
        const upperLimits = average + 50 * variance
        const lowerLimits = average - 50 * variance
        return [lowerLimits, upperLimits]
      }
      function multiDataService(bond_cd, date, duration_days) {
        return new Promise(async (resolve, reject) => {
          const multiDataInstance = new MultiData(bond_cd, date, duration_days);
          try {
            await multiDataInstance.generateData(bond_cd, date, duration_days);
            resolve(multiDataInstance.dataPackage);
          } catch (error) {
            reject(error);
          }
        })
      }
      function getNetValueStats(items) {
        let maxNetValue = -Infinity;
        let minNetValue = Infinity;

        items.forEach(item => {
          if (item.netValue > maxNetValue) {
            maxNetValue = item.netValue;
          }
          if (item.netValue < minNetValue) {
            minNetValue = item.netValue;
          }
        });
        return [minNetValue, maxNetValue]
      }
      try {
        const dataPackage = await multiDataService(this.bond_cd, this.end_date, this.duration_days)
        // average and dev
        // console.log('dataPackage.transaction', dataPackage)
        // const scatter_data = dataPackage.transaction.map(item => item.netPrice)
        // const scatter_statistic = average_var(scatter_data)
        // const theLimits = upperLowerLimits(scatter_statistic)
        const mktPrice_data = dataPackage.mktPrice
        const theLimits = getNetValueStats(mktPrice_data)
        // console.log('theLimits:', theLimits)
        const clonedDataPackage = _.cloneDeep(dataPackage)
        this.drawMultiCharts(clonedDataPackage, this.bond_cd, this.end_date, this.duration_days, this, theLimits)
        return dataPackage
      } catch (error) {
        console.log('Error:', error)
      }
    }

  }
}
</script>
<style lang="scss" scoped>
#tooltip {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 10;
  margin: 0;
  // padding: 10px;
  width: 15px;
  height: 12px;
  color: white;
  font-family: sans-serif;
  font-size: 12px;
  font-weight: bold;
  text-align: center;
  background-color: rgba(0, 0, 0, 0.75);
  opacity: 0;
  pointer-events: none;
}

</style>
