import * as React from 'react';
import Button from '@mui/material/Button';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import FilledInput from '@mui/material/FilledInput';
import Visibility from '@mui/icons-material/Visibility';
import VisibilityOff from '@mui/icons-material/VisibilityOff';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import IconButton from '@mui/material/IconButton';
import InputAdornment from '@mui/material/InputAdornment';
import {orderDelete, startOrder, stopOrder, createOrder} from "../requests/Requests";


export default function FormDialog(props) {
  const { successText, openModal, closeModal, data, checkIndex, selectionModel} = props
  const [password, setPassword] = React.useState('');
  const [showPassword, setShowPassword] = React.useState(false);
  const [success, setSuccess] = React.useState(false);
  const [modalErrors, setModalErrors] = React.useState(null);

  React.useEffect(() => {
      setPassword('');
      setModalErrors(null);
  }, [openModal])

  const  deleteSelectedElement = async (d) => {
    console.log(selectionModel)
    if (selectionModel.length > 0){
      for (let order_id of selectionModel){
          const index = selectionModel.indexOf(order_id)
          await orderDelete({order_id, password})
              .then((r) => selectionModel.splice(index, 1))
              .then((data) => {
                setModalErrors(null);
                setSuccess(true);
                closeModal(true);
              })
              .catch((err) => {
                console.log(err.response.data);
                setModalErrors(err.response.data);
                setSuccess(false);
              });
      }
    }
  };

  const startSelectedElement = async (d) => {
      console.log(selectionModel)

      if (selectionModel.length > 0) {
          for (let order_id of selectionModel) {
              await startOrder({order_id, password})
                  .then((data) => {
                    setModalErrors(null);
                    setSuccess(true);
                    closeModal(true);
                  })
                  .catch((err) => {
                    console.log(err.response.data);
                    setModalErrors(err.response.data);
                    setSuccess(false);
                  });
          }
      }
  }

  const stopSelectedElement = async (d) => {
      if (selectionModel.length > 0){
          for (let order_id of selectionModel){
              await stopOrder({order_id, password})
                  .then((data) => {
                      setModalErrors(null);
                      setSuccess(true);
                      closeModal(true);
                  })
                  .catch((err) => {
                    console.log(err.response.data);
                    setModalErrors(err.response.data);
                    setSuccess(false);
                  });
      }
    }
  }

  const handleSubmit = async (event) => {
    event.preventDefault();
    const order_data = {...data, password}
    if (checkIndex === 0) {
        await deleteSelectedElement(order_data)
    } else if (checkIndex === 1) {
        await stopSelectedElement(order_data)
    } else if (checkIndex === 2) {
        await startSelectedElement(order_data)
    } else if (checkIndex === 10) {
        await createOrder(order_data)
            .then((data) => {
                      setModalErrors(null);
                      setSuccess(true);
                      closeModal(true);
                  })
            .catch((err) => {
              console.log(err.response.data);
              setModalErrors(err.response.data);
              setSuccess(false);
            });
    }
  }

  return (
      <Dialog open={!openModal} onClose={() => closeModal(true)}>
        <DialogTitle>Confirmation</DialogTitle>
        <DialogContent>
            {/*{success && <DialogContentText sx={{color: "green"}}>{successText}</DialogContentText>}*/}
            {modalErrors?.detail && <DialogContentText sx={{color: "red"}}>{modalErrors.detail}</DialogContentText>}
          <FormControl sx={{ m: 1, width: '25ch' }} variant="filled">
          <InputLabel htmlFor="filled-adornment-password">Password</InputLabel>
          <FilledInput
            id="filled-adornment-password"
            type={showPassword ? 'text' : 'password'}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            endAdornment={
              <InputAdornment position="end">
                <IconButton
                  aria-label={modalErrors?.password ? modalErrors.password:"Password"}
                  onClick={() => setShowPassword(!showPassword)}
                  edge="end"
                >
                  {showPassword ? <VisibilityOff /> : <Visibility />}
                </IconButton>
              </InputAdornment>
            }
          />
        </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => closeModal(true)}>Cancel</Button>
          <Button onClick={handleSubmit}>Confirm</Button>
        </DialogActions>
      </Dialog>
  );
}