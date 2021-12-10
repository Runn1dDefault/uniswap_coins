from uniswap import Uniswap
from web3 import Web3

from uniswap_backend.settings import (
    ADDRESS, PRIVATE_KEY, PROVIDER, GAS_ENDPOINT
)

web3_instance = Web3()

uniswap_instance = Uniswap(
    ADDRESS,
    PRIVATE_KEY,
    PROVIDER,
    version=2
)
