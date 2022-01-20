import {useEffect} from 'react';
import { DataGrid } from '@mui/x-data-grid';
import {ordersGet} from '../requests/Requests';

const columns = [
  { field: 'id', headerName: 'ID', width: 70},
  { field: 'tokens', headerName: 'Tokens', width: 200, sortable: false},
  { field: 'prices', headerName: 'Prices', width: 200, sortable: false},
  { field: 'status', headerName: 'Status', width: 200},
  { field: 'times', headerName: 'Times', width: 300, sortable: false},
  { field: 'contract', headerName: 'S-Contract', width: 400, sortable: false,
      description: 'The value of this field will appear after the transaction is completed'}
];

export default function DataTable(props) {
  const {
      setButtonIndex, selectionModel,
      setSelectionModel,
      orders, setOrders,
      setRowID
  } = props;

  useEffect(() => {
    ordersGet()
      .then((data) => setOrders(data.data))
      .catch((error) => {
        console.log(error);
      });
  }, []);

  return (
    <div style={{ height: 400, width: '100%' }}>
      <DataGrid
        rows={orders}
        columns={columns}
        pageSize={5}
        rowsPerPageOptions={[5, 10, 25, 50, 100]}
        checkboxSelection
        // selectionModel={}
        // isRowSelectable={
        //   (params) => params?.status !== 'Over without trade' || params?.status !== 'Success'
        // }
        onSelectionModelChange={(newSelectionModel) => {
          if (newSelectionModel.length > 0){
            setButtonIndex(2);
          } else {
              setButtonIndex(0);
          }
          setSelectionModel(newSelectionModel);
        }}
        selectionModel={selectionModel}
        onRowClick={(row) => setRowID(row.id)}
      />
    </div>
  );
}
