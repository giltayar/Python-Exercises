"""\
partial - implement functools.partial (from python 2.6)

Takes a function and values for some of its arguments and produces a new function
with only the remaining arguments left.

>> def foo(x,y,z): ...
>> f = partial(foo,1,z=3) # this binds x=1 (positional) and z=3 (by name)
>> f(2) # equivalent to foo(1,2,3)
"""

from functools import wraps
def partial(f,*a_to_bind,**kw_to_bind):
    @wraps(f)
    def wrapped(*a,**kw):
        a_final = a_to_bind + a
        kw_final = kw_to_bind
        kw_final.update(kw)
        return f(*a_final,**kw_final)
    wrapped.__name__ = 'partial_' + f.__name__
    return wrapped