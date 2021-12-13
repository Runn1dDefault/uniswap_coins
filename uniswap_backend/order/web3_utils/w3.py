# -*- coding: utf-8 -*-
from web3 import Web3
from web3.middleware import geth_poa_middleware


def get_web3_instance(url):
    w3 = Web3(Web3.HTTPProvider(url, request_kwargs={'timeout': 10}))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return w3


if __name__ == '__main__':
   w = get_web3_instance('ya.ru')
