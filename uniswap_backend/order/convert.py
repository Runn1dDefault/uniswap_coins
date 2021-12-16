from django.conf import settings
from order.services.instances import uniswap_instance


def token_check_address(token_address):
    if token_address != settings.BASE_TOKEN_ADDRESS:
        _address = uniswap_instance.w3.toChecksumAddress(token_address)
        _get_token = uniswap_instance.get_token(_address)
        return _get_token.address, _get_token.decimals
    return settings.BASE_TOKEN_ADDRESS, 18

