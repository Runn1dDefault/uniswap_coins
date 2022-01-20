import * as React from "react";
import { useTheme } from '@material-ui/core/styles';
import ReactApexChart from "react-apexcharts";


const ApexChart = (props) => {
    const {orderPrices} = props;
    const theme = useTheme();

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

    const createData = (data) => {
        const new_data = {
            series: [{
                data: data
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
        }
        setChartData(new_data)
    }

    React.useEffect(() => {
        createData(orderPrices)
    }, [orderPrices])

    return (
        <ReactApexChart options={chartData.options} series={chartData.series} type="candlestick" height={350}/>
    )
}


export default ApexChart;
