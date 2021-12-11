import multiprocessing
import random

from .instances import uniswap_instance


# decorator for new process. run -> method().start()
def multiprocess(func):

    def new_process(*args, **kwargs):
        process = multiprocessing.Process(
            name='%32x' % random.getrandbits(16*8),
            target=func,
            args=args,
            kwargs=kwargs
        )
        process.start()
        return func(*args, **kwargs)
    return new_process
