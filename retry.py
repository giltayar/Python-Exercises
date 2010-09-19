"""\
retry - a decorator that retries a function/method up to N times.

The wrapped function will exit with the return value of the first successful call, or
with the exception raised in the last attempt, if it failed N times.

>> @retry(3)
>> def foo(...)
"""

from functools import wraps
def retry(n_max):
    def deco(f):
        @wraps(f)
        def _wrapped(*a,**kw):
            for i in xrange(n_max):
                try:
                    return f(*a,**kw)
                except:
                    if i == n_max-1:
                        raise
        return _wrapped
    return deco
    