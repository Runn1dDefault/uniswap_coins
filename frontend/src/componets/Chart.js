import {useEffect, Fragment} from "react";
import { LineChart, Line, XAxis, YAxis, ResponsiveContainer, CartesianGrid, Tooltip } from 'recharts';
import {orderPricesGET} from '../requests/Requests';

export default function Chart(props) {
  const {
      orderPrices,
      rowID, createData
  } = props

  useEffect(() => {
    orderPricesGET(rowID)
        .then((resp) => createData(resp.data))
        .catch((err) => console.log(err))
  }, [rowID]);

  return (
    <Fragment>
      <ResponsiveContainer>
        <LineChart width={600} height={300} data={orderPrices} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
          <Line type="monotone" dataKey="price" stroke="#8884d8" />
          <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
        </LineChart>
      </ResponsiveContainer>
    </Fragment>
  );
}