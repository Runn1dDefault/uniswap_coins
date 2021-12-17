from django.conf import settings
from order.services.instances import get_uniswap_instance

_BASES_TOKENS_ADDRESSES = [
    settings.BASE_TOKEN_ADDRESS
]


def token_check_address(token_address, is_test: bool = False):
    if token_address not in _BASES_TOKENS_ADDRESSES:
        _address = get_uniswap_instance(is_test).w3.toChecksumAddress(token_address)
        _get_token = get_uniswap_instance(is_test).get_token(_address)
        return _get_token.address, _get_token.decimals
    return token_address, 18
