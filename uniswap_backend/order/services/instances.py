from uniswap import Uniswap
from uniswap_backend.settings import (ADDRESS, PRIVATE_KEY, PROVIDER)

from web3 import Web3
from web3.middleware import geth_poa_middleware


def get_web3_instance():
    w3 = Web3(Web3.HTTPProvider(PROVIDER, request_kwargs={'timeout': 10}))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return w3


uniswap_instance = Uniswap(
    ADDRESS,
    PRIVATE_KEY,
    PROVIDER,
    version=2,
    web3=get_web3_instance()
)


