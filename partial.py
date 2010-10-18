"""\
partial - implement functools.partial (from python 2.6)

Takes a function and values for some of its arguments and produces a new function
with only the remaining arguments left.

>> def foo(x,y,z): ...
>> f = partial(foo,1,z=3) # this binds x=1 (positional) and z=3 (by name)
>> f(2) # equivalent to foo(1,2,3)
"""

from functools import wraps

def partial(function, *partial_args, **partial_kwds):
    @wraps(function)
    def wrapper(*args, **kwds):
        final_kwds = dict(partial_kwds)
        final_kwds.update(kwds)
        return function(*(partial_args + args), **final_kwds)
    
    return wrapper