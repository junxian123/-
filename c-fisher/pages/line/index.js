import * as echarts from '../../ec-canvas/echarts';
import {DriftModel} from '../../models/drift.js'
const driftModel = new DriftModel()
async function initChart(canvas, width, height) {
	const res = await driftModel.countGifted()
	const timeArr = []
	const countArr = []
	res.forEach(item => {
		timeArr.push(item.time)
		countArr.push(item.count)
	})
    const chart = echarts.init(canvas, null, {
        width: width,
        height: height
    });
    canvas.setChart(chart);

    var option = {
        title: {
            text: '赠送图书情况（只显示10天记录）',
            left: 'center'
        },
        color: ["#37A2DA", "#67E0E3", "#9FE6B8"],
        grid: {
            containLabel: true
        },

        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: timeArr,
            // show: false
        },
        yAxis: {
            x: 'center',
            type: 'value',
            splitLine: {
                lineStyle: {
                    type: 'dashed'
                }
            }
            // show: false
        },
        series: [{
            type: 'line',
            smooth: true,
            data: countArr
        }, ]
    };

    chart.setOption(option);
    return chart;
}

Page({
    data: {
        ec: {
            onInit: initChart
        }
    },

    onReady() {}
});