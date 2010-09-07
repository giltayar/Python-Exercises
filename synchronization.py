"""\
Synchronization - utilities for running a method or code block as a "critical section"

synchronize_using is a context manager that accepts a lock:
>> lock = threading.RLock() # obviously this lock should be shared by all callers
>> ...
>> with synchronize_using(lock):
>>     ... # no callers using same lock will run this code in parallel

synchronized is a method decorator that runs the method after acquiring the mutex self._lock

>> class A(object):
>>     def __init__(self,...):
>>         self._lock = threading.RLock()
>>         ...
...
>>     @synchronized
>>     def foo(self,...):
>>         ... # no two calls will run in parallel

"""
