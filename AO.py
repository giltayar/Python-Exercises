"""\
AO - Implements the ActiveObject pattern.
Wraps a standard object, so that calls to it are executed asyncronously in a separate thread or threads
owned by the active object, making the object an in-process "server".

For calls that return a result, a Future (see future.py) is returned instead, and the result
can be obtained from the future object when it's ready.

Simple usage:
>> class A(object):
>>    ...
>> a = A(...) # create passive object
>> ao = AO(a) # wrap it with AO
>> ao.start() # start the AO's thread
>> ...
>> f = ao.foo(1,2,3) # calls a.foo in AO's thread
>> ...
>> result = f.get() # block until result is ready and get it (in real life scenarios we'd use an observer instead of blocking)

For more detailed description of the interface, see the unit tests.
"""
