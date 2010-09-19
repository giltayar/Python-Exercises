"""\
Tracer - wraps an object and provides tracing for all method calls.
Depends on DynamicProxy.

>> x = MyClass(...)
>> tracer = Tracer(x,logger)
>> tracer.foo(...) # calls x.foo, and sends trace of call and return value to the logger

"""
from dynamic_proxy import DynamicProxy

class Tracer(DynamicProxy):
    def __init__(self,obj,logger):
        super(Tracer,self).__init__()
        self.obj = obj
        self.logger = logger
        
    def _dispatch(self,method_name,*a,**kw):
        self.logger("%s called with a=%s, kw=%s" % (method_name,a,kw))
        mth = getattr(self.obj,method_name)
        res = mth(*a,**kw)
        self.logger("%s returned %s" % (method_name,res))
        return res