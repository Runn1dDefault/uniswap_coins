import React, {useEffect, useState} from "react";
import {createTheme, ThemeProvider} from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import ApexChart from "../componets/ApexChart";
import DataTable from '../componets/Orders';
import SwapForm from '../componets/SwapForm';
import ButtonsBar from '../componets/BottonsBar';
import {orderPricesGET, ordersGet} from "../requests/Requests";

const mdTheme = createTheme();

function DashboardContent() {
  const [buttonIndex, setButtonIndex] = useState(0);
  const [selectionModel, setSelectionModel] = useState([]);
  const [orders, setOrders] = useState([]);
  const [orderPrices, setOrderPrices] = useState([]);
  const [rowID, setRowID] = useState(0);
  const [count, setCount] = useState(0);

  function createData(data) {
    const newData = data.map((d) => {
        const price = parseFloat(d.price)
        const meanPrice = parseFloat(d.mean_price)
        if (price <= meanPrice) {
            return {
                x: new Date(d.date),
                y:[parseFloat(d.min_price), price, meanPrice, parseFloat(d.max_price)]
            }
        } else {
            return {
                x: new Date(d.date),
                y:[parseFloat(d.min_price), meanPrice, price, parseFloat(d.max_price)]
            }
        }
    })
    setOrderPrices(newData);
}

  useEffect(() => {
    const interval = setInterval(() => {
      setCount(count + 1);
      ordersGet()
        .then((resp) => setOrders(resp.data))
        .catch((error) => console.log(error.response))
      orderPricesGET(rowID)
        .then((resp) => {
            console.log(resp.data)
            createData(resp.data)
        })
        .catch((error) => console.log(error.response))
    }, 10000);
    return () => clearInterval(interval);
  }, [buttonIndex !== 1 && count]);

  return (
    <ThemeProvider theme={mdTheme}>
      <Box sx={{ display: 'flex' }}>
        <CssBaseline />
        <Box
          component="main"
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
          {buttonIndex === 0 | buttonIndex === 2 | buttonIndex === 4 | buttonIndex === 6 &&
          <Container sx={{ display: 'flex', mt: 4, mb: 4 }}>
            <Grid container spacing={3}>
              {/* Charts */}
              <Grid item xs={12}>
                <Paper
                  sx={{
                    p: 2,
                    display: 'flex',
                    flexDirection: 'column',
                    height: 390,
                  }}
                >
                    <ApexChart orderPrices={orderPrices}/>
                </Paper>
              </Grid>
              {/* Orders */}
              <Grid item xs={12}>
                <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
                  <DataTable
                      setRowID={setRowID}
                      setButtonIndex={setButtonIndex}
                      selectionModel={selectionModel} setSelectionModel={setSelectionModel}
                      orders={orders} setOrders={setOrders}
                      orderPrices={orderPrices} setOrderPrices={setOrderPrices}
                  />
                </Paper>
              </Grid>
            </Grid>
          </Container>}
          {/*  Swap Form */}
          {buttonIndex === 1 && <SwapForm/>}
            <ButtonsBar
                setButtonIndex={setButtonIndex} buttonIndex={buttonIndex}
                selectionModel={selectionModel} setSelectionModel={setSelectionModel}
                setOrders={setOrders}
            />
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default function Dashboard() {
  return <DashboardContent />;
}
