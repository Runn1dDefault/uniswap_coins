import * as React from "react";
import { useTheme } from '@material-ui/core/styles';
import ReactApexChart from "react-apexcharts";


const ApexChart = (props) => {
    const {orderPrices} = props;
    const theme = useTheme();
    
    React.useEffect(() => {
        setChartData(
            {
            series: [{
                data: orderPrices
            }],
            options: {
                chart: {
                    type: 'candlestick',
                    height: 350
                },
                title: {
                    text: 'CandleStick Chart',
                    align: 'left'
                },
                xaxis: {
                    type: 'datetime'
                },
                yaxis: {
                    tooltip: {
                        enabled: true
                    }
                }
            },
        })
    }, [orderPrices])
    
    const [chartData, setChartData] = React.useState({
            series: [{
                data: orderPrices
            }],
            options: {
                chart: {
                    type: 'candlestick',
                    height: 350
                },
                title: {
                    text: 'CandleStick Chart',
                    align: 'left'
                },
                xaxis: {
                    type: 'datetime'
                },
                yaxis: {
                    tooltip: {
                        enabled: true
                    }
                }
            },
    })
    return (
        <ReactApexChart options={chartData.options} series={chartData.series} type="candlestick" height={350}/>
    )
}


export default ApexChart;
