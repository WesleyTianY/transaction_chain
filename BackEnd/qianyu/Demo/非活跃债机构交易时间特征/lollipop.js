// set the dimensions and margins of the graph
const margin = {top: 10, right: 10, bottom: 10, left: 10},
    width = 800 - margin.left - margin.right,
    height = 200 - margin.top - margin.bottom;

const formatDateTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
};

// Parse the Data
d3.csv("instn_trader_trades_data.csv", function(d) {
    return {
        ...d,
        trade_time: new Date(d.trade_time),  // 解析时间字符串
        bond_amount: +d.bond_amount,  // 转换为数字
        trade_price: +d.trade_price     // 转换为数字
    };
}).then(function(data) {
    // console.log('data:', data);

    // 抽取数据中出现过的所有机构和交易员的组合,每个组合是一个列表
    const tradingStats = data.reduce((acc, d) => {
        const key = `${d.institution_name}-${d.trader_name}`;
        
        if (!acc[key]) {
            acc[key] = {
                institution: d.institution_name,
                trader: d.trader_name,
                tradeCount: 0,
                totalAmount: 0
            };
        }
        
        acc[key].tradeCount += 1;
        acc[key].totalAmount += +d.bond_amount || 0;
        
        return acc;
    }, {});
    
    // 转换为数组形式
    const instn_trader_list = Object.values(tradingStats);
    // console.log(instn_trader_list);

    let minTradePrice = Infinity, maxTradePrice = -Infinity,
        minBondAmount = Infinity, maxBondAmount = -Infinity,
        minTradeTime = new Date('2099-12-31').getTime(), maxTradeTime = new Date('1970-01-01').getTime();

    const instn_trader_data = instn_trader_list.map( item => {
        if (item.tradeCount > 0) {
            
            const newitem = {
                institution: item.institution,
                trader: item.trader,
                transaction: data.filter( x => x.institution_name === item.institution && x.trader_name === item.trader)
            };
            minTradePrice = Math.min(minTradePrice, d3.min(newitem.transaction, d => d.trade_price));
            maxTradePrice = Math.max(maxTradePrice, d3.max(newitem.transaction, d => d.trade_price));

            minBondAmount = Math.min(minBondAmount, d3.min(newitem.transaction, d => d.bond_amount));
            maxBondAmount = Math.max(maxBondAmount, d3.max(newitem.transaction, d => d.bond_amount));

            minTradeTime = Math.min(minTradeTime, d3.min(newitem.transaction, d => d.trade_time.getTime()));
            maxTradeTime = Math.max(maxTradeTime, d3.max(newitem.transaction, d => d.trade_time.getTime()));

            return newitem;
        }
        return null;  // 显式返回null
    }).filter(item => item !== null);  // 过滤掉null值

    // console.log(instn_trader_data);

    // 所有交易的数额的最大值，时间的上下限（取整）
    const zeroPrice = 3/2 * minTradePrice - 1/2 * maxTradePrice;
    console.log('minTradeTime:', formatDateTime(minTradeTime), 'maxTradeTime:', formatDateTime(maxTradeTime));


    // X axis
    const x = d3.scaleTime()
            .range([ margin.left, width-margin.right ])
            .domain([minTradeTime, maxTradeTime]);

    // Y axis 价格
    const y = d3.scaleLinear()
                .range([height/2, height])
                .domain([zeroPrice, maxTradePrice]);
    // const dirct = value => value === "buy" ? -1 : 1;
    // console.log(y(zeroPrice), y(maxTradePrice), 2 * y(zeroPrice) - y(maxTradePrice));

    // r scale 交易量
    const r = d3.scaleLog()
                .range([ 2, 10 ])
                .domain([minBondAmount, maxBondAmount]);

    const color = value => value === "buy" ? "green" : "red";

    // 绘制每个机构-交易员组合的lollipop图
    instn_trader_data.forEach( (item, index) => {
        const box = d3.select("#my_dataviz").append("div").attr("class", "lollipop-box");
        box.append("h4").text(`${item.institution}-${item.trader}`);
        const container = box.append("div")
                            .attr("class", "lollipop")
                            .attr("id", `lollipop-${index}`);
        const svg = container.append("svg")
                            .attr("viewBox", [0, 0, width, height]);
        const g = svg.append("g");

        const lolli_data = item.transaction.sort( (a, b) => 
            d3.ascending(a.trade_time, b.trade_time) 
        );
        // console.log(lolli_data);

        const lollipops = g.selectAll("g.lollipop")
                            .data(lolli_data)
                            .join("g")
                            .attr("class", "lollipop")
                            .attr('opacity', 0.5);
        lollipops.append("line")
                .attr("x1", d => x(d.trade_time))
                .attr("x2", d => x(d.trade_time))
                .attr("y1", d => {
                    if (d.trade_direction === "buy") {
                        return y(d.trade_price);
                    } else {
                        return 2 * y(zeroPrice) - y(d.trade_price);
                    }
                })
                // .attr("y1", d => 2 * y(zeroPrice) - y(d.trade_price))
                .attr("y2", y(zeroPrice))
                .attr("stroke", d => color(d.trade_direction));

        lollipops.append("circle")
                .attr("cx", d => x(d.trade_time))
                .attr("cy", d => {
                    if (d.trade_direction === "buy") {
                        return y(d.trade_price);
                    } else {
                        return 2 * y(zeroPrice) - y(d.trade_price);
                    }
                })
                // .attr("cy", d => 2 * y(zeroPrice) - y(d.trade_price))
                .attr("r", d =>{ 
                    // if ( r(d.trade_price) >3 ) console.log(d.trade_price);
                    return r(d.bond_amount)
                })
                .style("fill", d => color(d.trade_direction))
                .attr("stroke", "black");

    });
 
});