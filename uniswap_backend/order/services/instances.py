from uniswap import Uniswap
from web3.gas_strategies.time_based import fast_gas_price_strategy

from uniswap_backend.settings import (ADDRESS, PRIVATE_KEY, PROVIDER, TEST_PROVIDER)

from web3 import Web3, middleware
from web3.middleware import geth_poa_middleware


def get_web3_instance():
    w3 = Web3(Web3.HTTPProvider(PROVIDER, request_kwargs={'timeout': 10}))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    # gas strategy
    w3.eth.set_gas_price_strategy(fast_gas_price_strategy)
    w3.middleware_onion.add(middleware.time_based_cache_middleware)
    w3.middleware_onion.add(middleware.latest_block_based_cache_middleware)
    w3.middleware_onion.add(middleware.simple_cache_middleware)
    return w3


def get_uniswap_instance(test_provider: bool = False):
    if test_provider:
        provider = TEST_PROVIDER
    else:
        provider = PROVIDER

    return Uniswap(
        address=ADDRESS,
        private_key=PRIVATE_KEY,
        provider=provider,
        version=2,
        web3=get_web3_instance()
    )



