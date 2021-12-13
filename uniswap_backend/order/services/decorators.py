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


def auto_change_version(func):
    """
        If none of the versions was successful, then an error will be displayed
    """
    uniswap_instance.version = 1

    def change_version(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            if uniswap_instance.version == 3:
                raise Exception(e)
            elif uniswap_instance.version == 1:
                uniswap_instance.version = 2
            else:
                uniswap_instance.version = 3

            result = change_version(*args, **kwargs)

        return result
    return change_version
