import React,{useState, useEffect} from 'react';
import {searchToken, createOrder} from '../requests/Requests';
import styled from "styled-components";
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Autocomplete from '@mui/material/Autocomplete';
import { DoneAllOutlined } from "@material-ui/icons";

const theme = createTheme();

export default function SwapForm() {
  const [errors, setErrors] = useState(null);
  // tokens lists
  const [tokens_in, setITokens] = useState([]);
  const [tokens_out, setOTokens] = useState([]);
  // inputs data
  const [token_in, setTokenIn] = useState("");
  const [tiCount, setTICount] = useState(0);
  const [token_out, setTokenOut] = useState("");
  const [toCount, setTOCount] = useState(0);
  const [times, setTimes] = useState("");
  const [percentage, setPercentage] = useState(1);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    setITokens(base_tokens);
    setOTokens(base_tokens);
  }, []);

  const handleSubmit = (event) => {
    event.preventDefault();
    const data = {
      token_from: token_in,
      token_to: token_out,
      count_from: tiCount,
      count_to: toCount,
      times: times,
      percentage: percentage
    }
    console.log(data);
    createOrder(data)
    .then((data) => setSuccess(true))
    .catch((error) => {
      console.log(error?.response?.data)
      setErrors(error?.response?.data);
      setSuccess(false);
    });
  };

  const options = (tokens_list) => {
    const tokens = tokens_list.map((token) => {
      const firstLetter = token.symbol[0].toUpperCase();
      return {
        firstLetter: /[0-9]/.test(firstLetter) ? '0-9' : firstLetter,
        ...token,
        };
      });
    return tokens
  }

  return (
    <Wrap>
    <ThemeProvider theme={theme}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          {success === true && <DoneAllOutlined style={{ color: "green" }} />}
          {errors?.non_field_errors && <p style={{color: "red"}}>{errors.non_field_errors}</p>}
          {errors?.detail && <p style={{color: "red"}}>{errors.detail}</p>}
          <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
            <div className='container'>
              <Autocomplete
                id="token_from"
                options={options(tokens_in).sort((a, b) => -b.firstLetter.localeCompare(a.firstLetter))}
                groupBy={(token) => token.firstLetter}
                getOptionLabel={(token) => {
                  setTokenIn(token.address)
                  return token.symbol
                }}
                sx={{ width: 400 }}
                onInputChange={(e) => {
                  setErrors(null);
                  if (e.target.value === ""){
                    setITokens(base_tokens);
                  } else {
                    searchToken(e.target.value)
                    .then((data) => {
                      setITokens(data.data);
                      })
                      .catch((e) => {
                        setITokens(base_tokens);
                      })
                  }
                }}
                renderOption={(props, option) => (
                  <Box component="li" sx={{ '& > img': { mr: 2, flexShrink: 0 } }} {...props}>
                    <img
                      loading="lazy"
                      width="20"
                      src={option.logoURI}
                      srcSet={`${option.logoURI} 2x`}
                      alt=""
                    />
                    {option.symbol}
                  </Box>
                )}
                renderInput={(params) =>
                  <TextField
                    {...params}
                    label={errors?.token_from ? errors.token_from?.token_from || errors.token_from:"Token In"}
                    error={errors?.token_from ? true:false}
                  />
                }
              />
              <TextField
                label={errors?.count_from ? errors.count_from?.count_from || errors.count_from:"Quantity"}
                error={errors?.count_from ? true:false}
                type="number"
                value={tiCount}
                onChange={(e) => {
                  setTICount(e.target.value);
                  setErrors(null);
                }}
                InputLabelProps={{
                  shrink: true,
                }}
                variant="filled"
              />
            </div>
            <div class='container'>
              <Autocomplete
                id="token_to"
                options={options(tokens_out).sort((a, b) => -b.firstLetter.localeCompare(a.firstLetter))}
                groupBy={(token) => token.firstLetter}
                getOptionLabel={(token) => {
                  setTokenOut(token.address)
                  return token.symbol
                }}
                sx={{ width: 400 }}
                onInputChange={(e) => {
                  setErrors(null);
                  if (e.target.value === ""){
                    setOTokens(base_tokens);
                  } else {
                    searchToken(e.target.value)
                    .then((data) => {
                      setOTokens(data.data);
                      })
                      .catch((err) => {
                        setOTokens(base_tokens);
                      })
                  }
                }}
                renderOption={(props, option) => (
                  <Box component="li" sx={{ '& > img': { mr: 2, flexShrink: 0 } }} key={option.id} {...props}>
                    <img
                      loading="lazy"
                      width="20"
                      src={option.logoURI}
                      srcSet={`${option.logoURI} 2x`}
                      alt=""
                    />
                    {option.symbol}
                  </Box>
                )}
                renderInput={(params) =>
                <TextField
                  {...params}
                  label={errors?.token_to ? errors.token_to?.token_to || errors.token_to:"Token Out"}
                  error={errors?.token_to ? true:false}
                />
                }
              />
              <TextField
                label={errors?.count_to ? errors.count_to?.count_to || errors.count_to:"Quantity"}
                error={errors?.count_to ? true:false}
                type="number"
                value={toCount}
                onChange={(e) => {
                  setTOCount(e.target.value);
                  setErrors(null);
                }}
                InputLabelProps={{
                  shrink: true,
                }}
                variant="filled"
              />
            </div>
            <div id='time_range'>
              <TextField
                label={errors?.times ? errors.times?.times || errors.times:"Times"}
                error={errors?.times ? true:false}
                helperText="example: 1d 1h 1m"
                onChange={(e) => {
                  setTimes(e.target.value);
                  setErrors(null);
                }}
              />
              <TextField
                id="percentage"
                label="Percentage"
                value={percentage}
                onChange={(e) => setPercentage(e.target.value)}
                type="number"
                defaultValue='1'
                InputLabelProps={{
                  shrink: true,
                }}
                variant="filled"
              />
            </div>
            
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Create order Swap
            </Button>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
    </Wrap>
  );
}

const Wrap = styled.div`
  position: absolute;
  width: 100%;
  .container{
    display: flex;
    margin: 10px 0px;
  }
  #time_range{
    display: flex;
    margin: 10px 0px;
  }
`;

// Base Tokens

const base_tokens = [
  {
    chainId: 1,
    name: "Tether",
    address: "0xdac17f958d2ee523a2206206994597c13d831ec7",
    decimals: 6,
    symbol: "USDT",
    logoURI: "https://s2.coinmarketcap.com/static/img/coins/64x64/825.png"
  },
  {
    chainId: 1,
    name: "UNI COIN",
    address: "0xe6877ea9c28fbdec631ffbc087956d0023a76bf2",
    decimals: 18,
    symbol: "UNI",
    logoURI: "https://s2.coinmarketcap.com/static/img/coins/64x64/4113.png"
  },
  {
    chainId: 1,
    name: "Uniswap",
    address: "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984",
    decimals: 18,
    symbol: "UNI",
    logoURI: "https://s2.coinmarketcap.com/static/img/coins/64x64/7083.png"
  },
  {
    chainId: 1,
    name: "WETH",
    address: "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
    decimals: 18,
    symbol: "WETH",
    logoURI: "https://s2.coinmarketcap.com/static/img/coins/64x64/2396.png"
  },
  {
    chainId: 1,
    name: "Dai",
    address: "0x6b175474e89094c44da98b954eedeac495271d0f",
    decimals: 18,
    symbol: "DAI",
    logoURI: "https://s2.coinmarketcap.com/static/img/coins/64x64/4943.png"
  },
  {
    chainId: 1,
    name: "USD Coin",
    address: "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    decimals: 6,
    symbol: "USDC",
    logoURI: "https://s2.coinmarketcap.com/static/img/coins/64x64/3408.png"
  }
]