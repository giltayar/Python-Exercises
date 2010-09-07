"""\
cache decorator.

If the wrapped function/method is called with the same arguments as a previous call, then 
the result is returned from cache, instead of computing it again.
This is only applicable to functions which have no side effect, and that are stateless, i.e. where
the result depends only on the call's arguments.

>> @cache
>> def foo(x,y): ...
>> ...
>> foo(1,2) # first call with args 1,2. calls wrapped function and remembers the result
>> foo(2,3) # first call with args 2,3. calls wrapped function and remembers the result
>> foo(1,2) # returns result from cache. doesn't call wrapped function.
"""
