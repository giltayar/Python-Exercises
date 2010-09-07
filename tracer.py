"""\
Tracer - wraps an object and provides tracing for all method calls.
Depends on DynamicProxy.

>> x = MyClass(...)
>> tracer = Tracer(x,logger)
>> tracer.foo(...) # calls x.foo, and sends trace of call and return value to the logger

"""
