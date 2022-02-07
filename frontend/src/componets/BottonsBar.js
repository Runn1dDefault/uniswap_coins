import React from "react";
import PropTypes from "prop-types";
import {useTheme} from '@mui/material/styles';
import Zoom from "@mui/material/Zoom";
import {green} from "@mui/material/colors";
import Fab from "@mui/material/Fab";
import AddIcon from "@mui/icons-material/Add";
import DashboardIcon from "@mui/icons-material/Dashboard";
import DeleteIcon from "@material-ui/icons/Delete";
import StopIcon from "@mui/icons-material/Stop";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import MeetingRoomIcon from '@mui/icons-material/MeetingRoom';
import {ordersGet} from "../requests/Requests";
import {logoutRequest} from "../requests/AuthRequests";


function useOutside(ref, setter, value) {
    React.useEffect(() => {
        function handleClickOutside(event) {
            if (ref.current && !ref.current.contains(event.target)) {
                setter(value)
            }
        }
        document.addEventListener("mousedown", handleClickOutside);
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, [setter, ref]);
}

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
  const {rowID, buttonIndex, setButtonIndex, selectionModel, setOrders, setCloseModal, setCheckIndex} = props;
  const out = React.useRef(null);
  useOutside(out, setButtonIndex, 0)

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
    console.log(index)
    event.preventDefault();
    if (index === 0 || index === 1 || index === 2){
        setCheckIndex(index);
        setCloseModal(false)
            .then((r) => {
                orderGetHandle().then((r) => {
                    selectionModel.splice(selectionModel.indexOf(rowID), 1);
                    if (index === 0) {
                        setButtonIndex(0)
                    }
                })
            })
    }
  }

  if (buttonIndex === 2) {
    return (
        <div ref={out}>
            {order_buttons.map((fab, index) => (
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
            )}
        </div>
    )
  }
  return (
      fabs.map((fab, index) => (
        <div>
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
            <Zoom
              key="logout_button"
              in={true}
              timeout={transitionDuration}
              style={{
                transitionDelay: `${buttonIndex === index ? transitionDuration.exit : 0}ms`,
              }}
              unmountOnExit
            >
              <Fab onClick={() => logoutRequest().then((d) => console.log('You are logout'))}
                   sx={{position: 'absolute', bottom: 80, right: 16}} aria-label="Logout" color="inherit">
                <MeetingRoomIcon/>
              </Fab>
            </Zoom>
         </div>
        ))
    );
}

FloatingActionButtonZoom.propTypes = {
  buttonIndex: PropTypes.number.isRequired
};
