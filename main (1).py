import os
import random
import datetime
import multiprocessing

from uniswap import Uniswap
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()


def multiprocess(func):

    def new_process(*args, **kwargs):
        process = multiprocessing.Process(
            name='%32x' % random.getrandbits(16*8),
            target=func,
            args=args,
            kwargs=kwargs
        )
        return process
    return new_process


uni_swap_wrapper = Uniswap(
    os.environ['ADDRESS'],
    os.environ['PRIVATE_KEY'],
    os.environ['PROVIDER'],
    None,
    2,
    float(os.environ['MAX_SLIPPAGE'])
)


@multiprocess
def get_price(token_from, token_to):
    input_ = uni_swap_wrapper.get_price_input(token_from, token_to, 10**18)
    output = uni_swap_wrapper.get_price_output(token_to, token_from, 10**18)

    # conversion = ((1/rate) * (usd_rate / 10 ** 6)) * (10 ** 18)

    print(datetime.datetime.now(), 'input', '${:,.2f}'.format(output / 10 ** 6))


if __name__ == '__main__':
    usdt = Web3.toChecksumAddress(os.environ['USDT'])
    # get_price(
    #     token_from=os.environ['ETH'],
    #     token_to=usdt
    # ).start()
    uni_swap_wrapper.version = 3
    print(uni_swap_wrapper.version)
    # get_price(os.environ['ETH'], os.environ['BAT']).start()
