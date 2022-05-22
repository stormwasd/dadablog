"""
@Description : 
@File        : decrator_examle
@Project     : BackEnd
@Time        : 2022/5/20 17:15
@Author      : LiHouJian
@Software    : PyCharm
@issue       : 
@change      : 
@reason      : 
"""
import time


def get_func_time(get_time):
    def wrapper():
        start = time.time()
        get_time()
        end = time.time()
        msecs = (end - start) * 1000
        print("time is %d ms" % (msecs))

    # return get_add(*args, **kwargs)
    return wrapper


# simpletest
@get_func_time  # get_time = get_func_time(get_time)
def get_time():
    print("hello")
    time.sleep(1)
    print("world")


get_time()
