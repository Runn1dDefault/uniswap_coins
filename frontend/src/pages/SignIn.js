import clsx from "clsx";
import React, { useState } from "react";
import styled from "styled-components";
import { Button } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import TextField from "@material-ui/core/TextField";
import Visibility from "@material-ui/icons/Visibility";
import VisibilityOff from "@material-ui/icons/VisibilityOff";
import OutlinedInput from "@material-ui/core/OutlinedInput";
import InputLabel from "@material-ui/core/InputLabel";
import InputAdornment from "@material-ui/core/InputAdornment";
import IconButton from "@material-ui/core/IconButton";
import FormControl from "@material-ui/core/FormControl";
import {loginRequest} from "../requests/AuthRequests";

const useStyles = makeStyles((theme) => ({
  root: {
    "& .MuiTextField-root": {
      margin: theme.spacing(1),
    },
  },
}));

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loginErrors, setLoginErrors] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    loginRequest({username, password})
      .then((data) => window.location.replace("/"))
      .catch((err) => {
        const error = err.response.data;
        if (error?.username || error?.password) {
          setLoginErrors({"username": error.username, "password": error.password})
        }
      });
  };

  const classes = useStyles();

  return (
    <Wrapper>
      <div className="login_content">
        <form
          className={classes.root}
          noValidate
          autoComplete="off"
          onSubmit={handleSubmit}
        >
          <Input
            label={loginErrors?.username ? loginErrors.username : "Username"}
            id="outlined-size-small"
            defaultValue=""
            variant="outlined"
            size="medium"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            error={loginErrors?.username ? true : false}
          />
          <StyledForm
            className={clsx(classes.margin, classes.textField)}
            variant="outlined"
          >
            <InputLabel htmlFor="outlined-adornment-password" className={loginErrors ? 'Mui-error': ""}>
              { loginErrors ? loginErrors.password: "Password"}
            </InputLabel>
            <OutlinedInput
              id="outlined-adornment-password"
              type={showPassword ? "text" : "password"}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              error={loginErrors?.password ? true : false}
              endAdornment={
                <InputAdornment position="end">
                  <IconButton
                    aria-label="toggle password visibility"
                    onClick={() => setShowPassword(!showPassword)}
                    onMouseDown={(e) => e.preventDefault()}
                    edge="end"
                  >
                    {showPassword ? <Visibility /> : <VisibilityOff />}
                  </IconButton>
                </InputAdornment>
              }
              labelWidth={loginErrors?.password ?  200:80}
            />
          </StyledForm>
          <Button
            type="submit"
            variant="contained"
            style={{
              marginTop: "10px",
              marginLeft: "11px",
              width: "100%",
              padding: "10px 20px",
            }}
          >
            Sign In
          </Button>
        </form>
      </div>
    </Wrapper>
  );
}

export default Login;

const Wrapper = styled.section`
  display: flex;
  height: 100vh;
  background: #ced6d9;
  width: 100%;
  justify-content: center;
  align-items: center;
  .signin_error {
    text-align: center;
    color: red;
  }
  .wrapper {
    display: flex;
  }
  form {
    width: 350px;
    background: #fff;
    padding: 50px 50px;
    border-radius: 10px;
    color: #2d333a;
    .register {
      margin: 12px;
    }
    .icon {
      font-size: 50px;
      margin-right: 10px;
      justify-content: center;
      left: 50%;
    }
    .sign_up_with_google {
      padding: 10px 40px;
      border: 1px solid #0a0a0a;
      border-radius: 10px;
      background: #fff;
      outline: none;
      width: 80%;
      margin: 0 auto;
      color: red;
      display: flex;
      align-items: center;
      font-size: 17px;
      color: #0a0a0a;
      white-space: nowrap;
      cursor: pointer;
    }
    .form_title {
      text-align: center;
      display: flex;
      justify-content: center;
      align-items: center;
      color: #2d333a;
      line-height: 36px;
      font-weight: 800;
      font-size: 26px;
    }
    .form_text {
      font-weight: 400;
      font-size: 14px;
      line-height: 21px;
      text-align: center;
    }
    .form_text_ {
      margin: 30px 0;
      text-align: center;
      position: relative;
      :before {
        position: absolute;
        content: "";
        top: 50%;
        width: 50%;
        height: 1px;
        right: -20px;
        background: #0a0a0a;
      }
      :after {
        position: absolute;
        content: "";
        top: 50%;
        width: 50%;
        height: 1px;
        left: -20px;
        background: #0a0a0a;
      }
    }
    @media (max-width: 768px) {
      padding: 30px;
      width: 100%;
    }
  }
`;

const Input = styled(TextField)`
  width: 100%;
  background: #fff;
  border-radius: 7px;
  outline: none;
  margin-bottom: 25px;
`;
const StyledForm = styled(FormControl)`
  width: 100%;
  background: #fff;
  border-radius: 7px;
  outline: none;
  margin-left: 10px;
  margin-top: 25px;
  margin-bottom: 25px;
`;