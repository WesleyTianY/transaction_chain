import axios from 'axios'
import Mock from 'mockjs' // Assuming you have Mock.js installed
import { format } from 'date-fns' // Assuming you have date-fns installed
// 数据的逻辑：
// 1. 遍历bondlist的中的cd，索取一整套数据包括所有的基础数据 按照 天数进行索取，存到Datapackage中去
// 2. 数据为一天的数据，上下午这个数据需要自己写函数进行拆分 dataDivide | for day in dataPackage
// 3. 每一天的数据为一个最小 package 需要对这一天的数据进行拆分拆为上午和下午，但这一步对用户应该不用可见，创建一个数据进行处理就可以了
// 4. 对最小数据包进行画图为一个函数，这个函数调用了5个子函数
// 5. datapackage的逻辑应该是按照bond_cd对数据进行查询得到的结果的集合，前端向后端发送bond_cd_list,后端按照list以及时间到数据库中调取数据。
// 6. 目前后端逻辑就按照前端发送的bond cd list后端发送相应的数据就好
// 对每个bond分别画图，分为早上和下午的，需要分别贴进去得到1天的数据
// date:结束日期 duration_days:持续天数
// Data Structure
// - dataPackage
//   - MktPrice
//   - Valuation
//   - Transaction
//   - Volume
//       - 横轴：原数据
//       - 纵轴：生成
//   - GradTimeline（生成）
//       - MktPrice Grad
//       - Volume Grad
class MultiData {
  constructor() {
    this.dataPackage = {
      mktPrice: [],
      transaction: [],
      valuation: [],
      volume: [],
      gradient: [],
      mktPriceTrue: []
      // mktPrice_flask: [],
      // transaction_flask: []
    }
    // this.generateData(bond_cd, date, duration_days)
  }
  async generateData(bond_cd, date, duration_days) {
    try {
      const mktPrice = await this.getMarketPriceData(bond_cd)
      const transaction = await this.getTransactionData(bond_cd)
      const valuation = await this.getValuationData(bond_cd)
      const volume = valuation
      this.dataPackage.mktPrice = mktPrice
      this.dataPackage.transaction = transaction
      this.dataPackage.valuation = valuation
      this.dataPackage.volume = volume
    } catch (error) {
      console.error('Error generating data:', error)
    }
  }
  async getValuationData(bond_cd) {
    try {
      const response = await axios.get(`http://localhost:5003/api/BasicData_Valuation/${bond_cd}`)
      // const transactionData = response.data.filtered_json_transaction
      const val = response.data.filtered_json_val
      return val
    } catch (error) {
      console.error('Error fetching market price data:', error)
      return []
    }
  }
  async getMarketPriceData(bond_cd) {
    try {
      const response = await axios.get(`http://localhost:5003/api/BasicData_MarketPrice/${bond_cd}`)
      // const transactionData = response.data.filtered_json_transaction
      const mktData = response.data.filtered_json_mkt
      return mktData
    } catch (error) {
      console.error('Error fetching market price data:', error)
      return []
    }
  }
  async getTransactionData(bond_cd) {
    try {
      const response = await axios.get(`http://localhost:5003/api/BasicData_transaction/${bond_cd}`)
      const transactionData = response.data.filtered_json_transaction
      return transactionData
    } catch (error) {
      console.error('Error fetching market price data:', error)
      return []
    }
  }
  updatedata(dataPackage) {
    // 给定时间戳字符串
    // const timestampString = '2023-07-05 17:29:38+08:00'
    // const originalDate = new Date(timestampString)
    // console.log('originalDate', originalDate)
    // 解析时间戳字符串
    // const parsedDate1 = parseTimestampString(timestampString)
    // const parsedDate2 = formatDateToCustomString(timestampString)
    // const parsedDate3 = formatDateToCustomDateString(timestampString)
    const mktPrice_flask = dataPackage.mktPrice_flask
    const transaction_flask = dataPackage.transaction_flask

    // function parseTimestampString(timestampString) {
    //   // 使用正则表达式从时间戳字符串中提取日期和时间部分
    //   const match = timestampString.match(/(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})\+(\d{2}:\d{2})/)

    //   if (match) {
    //     const datePart = match[1]
    //     const timezonePart = match[2]

    //     // 创建包含日期和时间的字符串
    //     const fullDateString = datePart + timezonePart

    //     // 使用Date构造函数将字符串转换为日期对象
    //     return new Date(fullDateString)
    //   }

    //   return null // 如果无法解析时间戳字符串，返回null或其他错误处理方式
    // }
    // function formatDateToCustomString(dateString) {
    //   const originalDate = new Date(dateString)

    //   const year = originalDate.getFullYear()
    //   const month = (originalDate.getMonth() + 1).toString().padStart(2, '0')
    //   const day = originalDate.getDate().toString().padStart(2, '0')
    //   const hours = originalDate.getHours().toString().padStart(2, '0')
    //   const minutes = originalDate.getMinutes().toString().padStart(2, '0')
    //   const seconds = originalDate.getSeconds().toString().padStart(2, '0')

    //   const formattedDate = `${year}_${month}_${day}_${hours}_${minutes}_${seconds}`
    //   return formattedDate
    // }
    // function formatDateToCustomDateString(dateString) {
    //   const originalDate = new Date(dateString)

    //   const year = originalDate.getFullYear()
    //   const month = (originalDate.getMonth() + 1).toString().padStart(2, '0')
    //   const day = originalDate.getDate().toString().padStart(2, '0')
    //   const hours = originalDate.getHours().toString().padStart(2, '0')
    //   const minutes = originalDate.getMinutes().toString().padStart(2, '0')
    //   const seconds = originalDate.getSeconds().toString().padStart(2, '0')

    //   const formattedDate = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
    //   return formattedDate
    // }
    // mktPrice_flask.forEach(function(d) { d.timeStamp = parseTime(d.timeStamp) })
    mktPrice_flask.then(function(result) {
      dataPackage.mktPrice = result
      console.log('mktPrice_flask parsedDate', result) // "Some User token"
    })
    transaction_flask.then(function(result) {
      dataPackage.transaction = result
      console.log('transaction_flask parsedDate', result) // "Some User token"
    })
    console.log('parsedDate dataPackage:', dataPackage)
    return dataPackage
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
          'transactionId': Mock.Random.string('upper', 3, 7),
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
export default MultiData
