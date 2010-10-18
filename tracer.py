"""\
Tracer - wraps an object and provides tracing for all method calls.
Depends on DynamicProxy.

>> x = MyClass(...)
>> tracer = Tracer(x,logger)
>> tracer.foo(...) # calls x.foo, and sends trace of call and return value to the logger

"""
from dynamic_proxy import DynamicProxy

class Tracer(DynamicProxy):
    def __init__(self, object, logger):
        self.object = object
        self.logger = logger
        
    def _dispatch(self, function_name, *args, **kwds):
        self.logger("%s called with a=%r, kw=%r" % (function_name, args, kwds))
        
        ret = getattr(self.object, function_name)(*args, **kwds)
        
        self.logger("%s returned %s" % (function_name, ret))
        
        return ret
    
    
