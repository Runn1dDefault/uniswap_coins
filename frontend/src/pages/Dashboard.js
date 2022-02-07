import React, {useEffect, useState} from "react";
import {createTheme, ThemeProvider} from '@mui/material/styles';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import DataTable from '../componets/Orders';
import SwapForm from '../componets/SwapForm';
import ButtonsBar from '../componets/BottonsBar';
import {ordersGet, orderPricesGET, orderTxsGET} from "../requests/Requests";
import ApexChart from "../componets/ApexChart";
import PinnedSubheaderList from "../componets/OrderTxs";
import FormDialog from "../componets/Modal";

const mdTheme = createTheme();


function DashboardContent() {
  const [buttonIndex, setButtonIndex] = useState(0);
  const [selectionModel, setSelectionModel] = useState([]);
  const [orders, setOrders] = useState([]);
  const [orderPrices, setOrderPrices] = useState([]);
  const [orderTxs, setOrderTxs] = useState([]);
  const [rowID, setRowID] = useState(0);
  const [count, setCount] = useState(0);
  const [closeModal, setCloseModal] = useState(true);
  const [checkIndex, setCheckIndex] = useState(5);

  function createData(data) {
      const chartData = data.map((item) => (
          {
              x: new Date(parseFloat(item.date) * 1000),
              y: [parseFloat(item.open), parseFloat(item.max_price), parseFloat(item.min_price),
                  parseFloat(item.close)
              ]
          }
      ));
      setOrderPrices(chartData);
  }

  useEffect(() => {
    const interval = setInterval(() => {
      setCount(count + 1);
      if (buttonIndex !== 1){
          ordersGet()
          .then((r) => setOrders(r.data))
          .catch((e) => console.log(e.response))
      }
      if (rowID !== 0 && buttonIndex !== 1) {
          orderTxsGET(rowID)
            .then((resp) => setOrderTxs(resp.data))
            .catch((error) => console.log(error.response))
          orderPricesGET(rowID)
            .then((resp) => createData(resp.data))
            .catch((error) => console.log(error.response))
      }
    }, 5000);
    return () => clearInterval(interval);
  }, [count]);

  return (
    <ThemeProvider theme={mdTheme}>
      <Box sx={{ display: 'flex' }}>
        <Box
          sx={{
            backgroundColor: (theme) =>
              theme.palette.mode === 'light'
                ? theme.palette.grey[100]
                : theme.palette.grey[900],
            flexGrow: 1,
            height: '100vh',
            overflow: 'auto',
          }}
        >
            <FormDialog
                openModal={closeModal}
                selectionModel={selectionModel}
                closeModal={setCloseModal}
                data={{order_id: rowID}}
                checkIndex={checkIndex}
            />
          {buttonIndex === 0 || buttonIndex === 2 || buttonIndex === 4 ?
          <Container maxWidth="lg" sx={{mt: 4, mb: 4 }}>
            <Grid container spacing={3} sx={{display: 'flex'}}>
              <Grid item xs={12} md={8} lg={8}>
                <Paper
                  sx={{
                    p: 2,
                    display: 'flex',
                    flexDirection: 'column',
                    height: 390,
                  }}
                >
                    <DataTable
                      setRowID={setRowID}
                      setButtonIndex={setButtonIndex}
                      selectionModel={selectionModel} setSelectionModel={setSelectionModel}
                      orders={orders} setOrders={setOrders}
                      orderPrices={orderPrices} setOrderPrices={setOrderPrices}
                  />
                </Paper>
              </Grid>
              <Grid item xs={12} md={4} lg={4}>
                <Paper
                  sx={{
                    p: 2,
                    display: 'flex',
                    flexDirection: 'column',
                    height: 390,
                  }}
                >
                    <PinnedSubheaderList orderTxs={orderTxs}/>
                </Paper>
              </Grid>
              <Grid item xs={12}>
                <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
                  <ApexChart orderPrices={orderPrices}/>
                </Paper>
              </Grid>
            </Grid>
          </Container>: <SwapForm/>}
            <ButtonsBar
                rowID={rowID}
                setCloseModal={setCloseModal}
                setButtonIndex={setButtonIndex} buttonIndex={buttonIndex}
                selectionModel={selectionModel} setSelectionModel={setSelectionModel}
                setOrders={setOrders} setCheckIndex={setCheckIndex}
            />
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default function Dashboard() {
  return <DashboardContent />;
}
