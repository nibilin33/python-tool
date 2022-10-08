# coding: utf-8
import functools

def exception(func):
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except:
            print(func.__name__)

    return wrapper