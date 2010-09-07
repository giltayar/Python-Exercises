"""\
Future - a placeholder for a result that will be ready in the future.
Allows checking whether the result is ready, blocking until it is, or setting an observer
that will be notified with the result when it's ready.
(This class is most useful in conjunction with Active Object class - see AO.py)

Simple usage:
>> f = Future()
>> 
>> # from thread 1
>> f.set(3)
>>
>> # from thread 2
>> x = f.get()

For more detailed description of the interface, see the unit tests.
"""
