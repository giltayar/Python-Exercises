"""\
retry - a decorator that retries a function/method up to N times.

The wrapped function will exit with the return value of the first successful call, or
with the exception raised in the last attempt, if it failed N times.

>> @retry(3)
>> def foo(...)
"""

from functools import wraps

def retry(number_of_times):
    def ret(func):
        @wraps(func)
        def func_substitute(*args, **kwds):
            for i in xrange(number_of_times):
                try:
                    return func(*args, **kwds)
                except Exception as e:
                    if (i == number_of_times - 1):
                        raise
        return func_substitute
    return ret
    
    