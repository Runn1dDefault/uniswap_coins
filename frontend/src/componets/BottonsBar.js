import React, {useState} from "react";
import PropTypes from "prop-types";
import {useTheme} from '@mui/material/styles';
import Zoom from "@mui/material/Zoom";
import TextField from "@mui/material/TextField";
import {green} from "@mui/material/colors";
import Fab from "@mui/material/Fab";
import {DoneAllOutlined} from "@material-ui/icons";
import AddIcon from "@mui/icons-material/Add";
import DashboardIcon from "@mui/icons-material/Dashboard";
import DeleteIcon from "@material-ui/icons/Delete";
import StopIcon from "@mui/icons-material/Stop";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import {orderDelete, ordersGet, startOrder, stopOrder} from "../requests/Requests";

const fabStyle = {
  position: 'absolute',
  bottom: 16,
  right: 16,
};

const fabGreenStyle = {
  color: 'common.white',
  bgcolor: green[500],
  '&:hover': {
    bgcolor: green[600],
  },
};

export default function FloatingActionButtonZoom(props) {
  const theme = useTheme();
  const {buttonIndex, setButtonIndex, selectionModel, setOrders} = props;
  const [errors, setErrors] = useState(null);
  const [times, setTimes] = useState("");
  const [successColor, setSuccessColor] = useState("inherit");

  const  deleteSelectedElement = async () => {
    if (selectionModel.length > 0){
      for (let order_id of selectionModel){
          const index = selectionModel.indexOf(order_id)
          await orderDelete(order_id)
              .then((r) => selectionModel.splice(index, 1))
              .catch((e) => console.log(e))
      }
    }
  };

  const startSelectedElement = async () => {
      if (selectionModel.length > 0 && times) {
          const times_data = {"times": times}

          for (let order_id of selectionModel) {
              await startOrder(order_id, times_data)
                  .catch((e) => {
                     setErrors(e?.response?.data)
                     setSuccessColor("secondary");
                  })
          }
      }
  }

  const stopSelectedElement = async () => {
      if (selectionModel.length > 0){
          for (let order_id of selectionModel){
              await stopOrder(order_id)
                  .catch((e) => console.log(e))
      }
    }
  }
  const orderGetHandle = async () => {
      await ordersGet()
          .then((r) => setOrders(r.data))
          .catch((e) => console.log(e))
  }

  const transitionDuration = {
    enter: theme.transitions.duration.enteringScreen,
    exit: theme.transitions.duration.leavingScreen,
  };

  const fabs = [
    {
      color: 'inherit',
      sx: { ...fabStyle, ...fabGreenStyle },
      icon: <AddIcon />,
      label: 'Add Order',
    },
    {
      color: 'primary',
      sx: fabStyle,
      icon: <DashboardIcon />,
      label: 'View Orders',
    }
  ];

  const order_buttons = [
    {
      key: "3",
      color: 'secondary',
      sx: {position: 'absolute', bottom: 16, right: 16},
      icon: <DeleteIcon />,
      label: 'Delete Order',
    },
    {
      key: "4",
      color: 'success',
      sx: {position: 'absolute', bottom: 80, right: 16},
      icon: <StopIcon />,
      label: 'Stop Order',
    },
    {
      key: "5",
      color: 'primary',
      sx: {position: 'absolute', bottom: 144, right: 16},
      icon: <PlayArrowIcon />,
      label: 'Start Order',
    }
  ];

  const handleButton = (event, index) => {
    event.preventDefault();
    if (index === 0){
        deleteSelectedElement()
            .then((r) => orderGetHandle())
            .then((r) => setButtonIndex(0))
    } else if (index === 1){
        stopSelectedElement()
            .then((r) => orderGetHandle())
    } else if (index === 2){
        setButtonIndex(6)
    }
  }


  if (buttonIndex === 6){
      const elements = [
          {
              key: "input",
              element:
                  <TextField
                    label={errors?.times ? errors.times?.times || errors.times:"Times"}
                    error={errors?.times ? true:false}
                    sx={{position: 'absolute', bottom: 16, right: 80, background: "silver"}}
                    onChange={(e) => {
                      setTimes(e.target.value);
                      setErrors(null);
                    }}
                  />
          },
          {
              key: "button",
              element:
                  <Fab
                    onClick={() =>{
                        startSelectedElement()
                            .then((r) =>
                                orderGetHandle().then(r => setSuccessColor("primary"))
                            )
                    }}
                    sx={{position: 'absolute', bottom: 20, right: 16}}
                    aria-label="SET times" color={successColor}>
                    <DoneAllOutlined/>
                  </Fab>
          }
      ]
      return (
            elements.map((element, index) => (<Zoom
              key={element.key}
              in={true}
              timeout={transitionDuration}
              style={{
                transitionDelay: `${buttonIndex === 4 ? transitionDuration.exit : 0}ms`,
              }}
              unmountOnExit
            >
                {element.element}
            </Zoom>
            ))
      )
  }
  if (buttonIndex === 2) {
    return (
        order_buttons.map((fab, index) => (
            <Zoom
                  key={fab.color}
                  in={true}
                  timeout={transitionDuration}
                  style={{
                    transitionDelay: `${buttonIndex === index ? transitionDuration.exit : 0}ms`,
                  }}
                  unmountOnExit
            >
            <Fab
                onClick={(e) => handleButton(e, index)}
                data-id={fab.key} sx={fab.sx} aria-label={fab.label} color={fab.color}>
                {fab.icon}
            </Fab>
            </Zoom>
            )
        )
    )
  }
  return (
      fabs.map((fab, index) => (
        <Zoom
          key={fab.color}
          in={buttonIndex === index}
          timeout={transitionDuration}
          style={{
            transitionDelay: `${buttonIndex === index ? transitionDuration.exit : 0}ms`,
          }}
          unmountOnExit
        >
          <Fab onClick={() => {
              if (buttonIndex === 0) {
                  setButtonIndex(1)
              } else if (buttonIndex === 1) {
                  setButtonIndex(0)
              }
          }} sx={fab.sx} aria-label={fab.label} color={fab.color}>
            {fab.icon}
          </Fab>
        </Zoom>
        ))
    );
}

FloatingActionButtonZoom.propTypes = {
  buttonIndex: PropTypes.number.isRequired
};
