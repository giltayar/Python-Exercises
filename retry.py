"""\
retry - a decorator that retries a function/method up to N times.

The wrapped function will exit with the return value of the first successful call, or
with the exception raised in the last attempt, if it failed N times.

>> @retry(3)
>> def foo(...)
"""
