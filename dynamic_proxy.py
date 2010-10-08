"""\
DynamicProxy - a way to trap all method calls performed on an object.

If a class inherits from DynamicProxy, any method call to methods that aren't specifically 
implemented in the class will result in a call to _dispatch(method_name,*a,**kw)

_dispatch should be implemented by the inheriting class.
See tracer.py and AO.py for usage examples

>> class A(DynamicProxy):
>>     ...
>> a = A(...)
>> a.foo(1,2,x=3) # assuming foo is not implemented in A, this is equivalent to:
                  # a._dispatch('foo',1,2,x=3)
"""
import functools
class DynamicProxy(object):
    def __getattr__(self, name):
        @functools.wraps(self._dispatch)
        def wrapper(*args, **kwds):
            return self._dispatch(name, *args, **kwds)
        
        return wrapper