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

# import RLock as convenience, since it is usually used together with this module
from threading import RLock # PyFlakesIgnore

class synchronize_using(object):
    def __init__(self,lock):
        self.lock = lock

    def __enter__(self):
        self.lock.acquire()
        return self
           
    def __exit__(self, exc_type, exc_value, traceback):
        self.lock.release()
    
from functools import wraps        
def synchronized(f):
    @wraps(f)
    def wrapper(self,*a,**kw):
        with synchronize_using(self._lock):
            return f(self,*a,**kw)
    return wrapper
