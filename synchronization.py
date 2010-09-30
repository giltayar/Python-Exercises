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
import threading
from functools import wraps

def synchronize_using(lock):
    class Synchronization(object):
        def __enter__(self):
            lock.acquire()
        def __exit__(self, type, value, traceback):
            lock.release()
        
    return Synchronization()

def synchronized(f):
    @wraps(f)
    def wrapping(*args, **kwds):
        with synchronize_using(threading.RLock()):
            return f(*args, **kwds)
                               
    return wrapping
