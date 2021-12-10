import multiprocessing
import random

from .instances import uniswap_instance


# decorator for new process
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


def real_support(func):
    """
    change version from [1, 2, 3]
        if version not valid
    """
    def change_version(*args, **kwargs):
        try:
            result = func(args, **kwargs)
            return result
        except Exception:
            uniswap_instance.version = random.randint(1, 3)
            return change_version()

    return change_version
