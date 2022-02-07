import {useState, useEffect} from 'react';
import {searchToken, createOrder} from '../requests/Requests';
import styled from "styled-components";
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Autocomplete from '@mui/material/Autocomplete';
import Checkbox from '@mui/material/Checkbox';
import AllInclusiveIcon from '@mui/icons-material/AllInclusive';
import AllInclusiveOutlinedIcon from '@mui/icons-material/AllInclusiveOutlined';
import Tooltip from '@mui/material/Tooltip';
import ImportExportIcon from '@mui/icons-material/ImportExport';
import GetAppOutlinedIcon from '@mui/icons-material/GetAppOutlined';
import FormDialog from './Modal';

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
  const [sellPercentage, setSellPercentage] = useState(0.1);
  const [slippage, setSlippage] = useState(0.1);
  const [infinity, setInfinity] = useState(true);
  const [isTwoTx, setIsTwoTx] = useState(true);
  const [closeModal, setCloseModal] = useState(true);
  const [data, setData] = useState(null);

  useEffect(() => {
    setITokens(base_tokens);
    setOTokens(base_tokens);
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setData({token_from: token_in, count_from: tiCount, token_to: token_out, count_to: toCount,
      slippage: slippage, sell_percentage: sellPercentage,
      only_buy: !isTwoTx, is_revolving_trade: infinity
    });
    await createOrder(data).catch((err) => {
      const er = err.response.data
      if (!er?.token_from && !er?.token_to && !er?.count_from && !er?.count_to && !er?.slippage
          && !er?.sell_percentage && !er?.detail && er?.password){
        setErrors(null);
        setCloseModal(false);
      } else {
        setErrors(er);
      }
    })
  }

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

  const labelCheck = { sx: {mb: 5, mt: 1, ml: 2}, inputProps: { 'aria-label': 'GOOD UNTIL CANCELLED' } };

  return (
    <Wrap>
    <ThemeProvider theme={theme}>
      <FormDialog
          successText={'Success'}
          openModal={closeModal}
          checkIndex={10}
          closeModal={setCloseModal}
          data={data}
      />
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
                    label={errors?.token_from ? errors.token_from: "Token In"}
                    error={errors?.token_from ? true:false}
                    required
                  />
                }
              />
              <TextField
                label={errors?.count_from ? errors.count_from:"Quantity"}
                error={errors?.count_from ? true:false}
                type="number"
                value={tiCount}
                maxLength={20}
                onChange={(e) => {
                  setTICount(e.target.value);
                  setErrors(null);
                }}
                InputLabelProps={{
                  shrink: true,
                }}
                variant="filled"
                required
              />
            </div>
            <div className='container'>
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
                  label={errors?.token_to ? errors.token_to:"Token Out"}
                  error={errors?.token_to ? true:false}
                  required
                />
                }
              />
              <TextField
                label={errors?.count_to ? errors.count_to:"Quantity"}
                error={errors?.count_to ? true:false}
                type="number"
                value={toCount}
                maxLength={20}
                onChange={(e) => {
                  setTOCount(e.target.value);
                  setErrors(null);
                }}
                InputLabelProps={{
                  shrink: true,
                }}
                variant="filled"
                required
              />
            </div>
            <div id='time_range'>
              <TextField
                label={errors?.slippage ? errors.slippage:"slippage"}
                error={errors?.slippage ? true:false}
                sx={{width: 130}}
                type="number"
                value={slippage}
                onChange={(e) => {
                  setSlippage(e.target.value); setErrors(null)}
                }
                InputLabelProps={{shrink: true}}
                variant="filled"
                required
              />
              <TextField
                label={errors?.sell_percentage ? errors.sell_percentage:"Sell Percentage"}
                error={errors?.sell_percentage ? true:false}
                sx={{ml: 1, mr: 2, width: 130}}
                type="number"
                value={sellPercentage}
                onChange={(e) => {setSellPercentage(e.target.value); setErrors(null)}}
                InputLabelProps={{shrink: true}}
                variant="filled"
                required
              />
              <Tooltip title="GOOD UNTIL CANCELLED">
                <Checkbox
                    {...labelCheck}
                    defaultChecked
                    onChange={() => setInfinity(!infinity)}
                    icon={<AllInclusiveIcon />}
                    checkedIcon={<AllInclusiveOutlinedIcon />}
                />
              </Tooltip>
              <Tooltip title={isTwoTx === true ? "Only buy":"Buy then sell"}>
                <Checkbox
                  {...labelCheck}
                  defaultChecked
                  onChange={() => setIsTwoTx(!isTwoTx)}
                  icon={<GetAppOutlinedIcon />}
                  checkedIcon={<ImportExportIcon />}
                />
              </Tooltip>
            </div>
            <Button type="submit" fullWidth variant="contained" sx={{ mb: 2 }}>Create order</Button>
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