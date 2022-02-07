from decimal import Decimal

import requests
from eth_typing import ChecksumAddress


def get_tokens():
    response = requests.get("https://tokens.coingecko.com/uniswap/all.json", timeout=None)
    if response.status_code == 200:
        data = response.json()
        tokens_list = list()
        for tokens in data['tokens']:
            if tokens not in tokens_list:
                tokens_list.append(tokens)
                yield tokens


def get_price(tk1: ChecksumAddress, tk2: ChecksumAddress, chain_id: int, qty):
    url = f'https://api.uniswap.org/v1/quote?protocols=v2,v3&tokenInAddress={tk1}&tokenInChainId={chain_id}' \
          f'&tokenOutAddress={tk2}&tokenOutChainId={chain_id}&amount={qty}&type=exactIn'
    response = requests.get(url, headers={'origin': 'https://app.uniswap.org'}, timeout=None)
    if response.status_code == 200:
        return Decimal(response.json()['quoteDecimals'])
    else:
        print(response.status_code, 'Failed request')
