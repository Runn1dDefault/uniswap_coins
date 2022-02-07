import {useEffect, useCallback} from 'react';
import { DataGrid } from '@mui/x-data-grid';
import {ordersGet} from '../requests/Requests';


const columns = [
  { field: 'id', headerName: 'ID', width: 80},
  { field: 'tokens', headerName: 'Tokens', width: 200, sortable: false},
  { field: 'status', headerName: 'Status', width: 200},
  { field: 'prices', headerName: 'Prices', width: 250, sortable: false},
      // description: 'The value of this field will appear after the transaction is completed'}
];

export default function DataTable(props) {
  const {
      setButtonIndex, selectionModel,
      setSelectionModel,
      orders, setOrders,
      setRowID
  } = props;

  const escFunction = useCallback((event) => {
    if(event.keyCode === 27) {
      setButtonIndex(0)
    }
  }, [setButtonIndex]);

  useEffect(() => {
    document.addEventListener("keydown", escFunction, false);
    return () => {
      document.removeEventListener("keydown", escFunction, false);
    };
  }, [escFunction]);

  useEffect(() => {
    ordersGet()
      .then((data) => setOrders(data.data))
      .catch((error) => {
        console.log(error);
      });
  }, []);

  return (
    <div id="table" style={{ height: 400, width: '100%' }}>
      <DataGrid
        rows={orders}
        columns={columns}
        pageSize={5}
        onSelectionModelChange={(newSelectionModel) => {
          if (newSelectionModel.length > 0){
            setButtonIndex(2);
          } else {
              setButtonIndex(0);
          }
          setSelectionModel(newSelectionModel);
        }}
        selectionModel={selectionModel}
        onRowClick={(row, event) => {
            setRowID(row.id);

        }}
      />
    </div>
  );
}
