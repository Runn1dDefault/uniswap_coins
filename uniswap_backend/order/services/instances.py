from uniswap import Uniswap

from uniswap_backend.settings import (
    ADDRESS, PRIVATE_KEY, PROVIDER, GAS_ENDPOINT
)

uniswap_instance = Uniswap(
    ADDRESS,
    PRIVATE_KEY,
    PROVIDER,
    version=2
)
