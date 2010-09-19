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

import threading
from synchronization import synchronized
import assertions
import traceback

class Future(object):
    def __init__(self):
        self._event = threading._Event()
        self._lock = threading.RLock() # used by @synchronized decorator
        self._val = None
        self._exc = None
        self._lst_observers = []

    @synchronized
    def attach_observer(self,observer):
        """observer(future) is called when future is set.
           observers attached after future is set will be called immediately (from same thread)
        """
        if self.is_set():
            observer(self)
        else:
            self._lst_observers.append(observer)

    @synchronized
    def _set(self,val=None,exc=None):
        """Used internally to set either completion value or error"""
        assertions.fail_if(self.is_set(), "Future is already set")
        if exc is not None: # check exc and not val. value can be legitimately set to None.
            self._exc = exc
        else:
            self._val = val
        self._event.set()
        self._notify_observers()

    def _notify_observers(self):
        for obs in self._lst_observers:
            try:
                obs(self)
            except Exception, e:
                assertions.warn("Future got exception while calling observer.", observer=obs, exc=traceback.format_exc(e))

    def set(self,val): self._set(val=val)
    def set_error(self,exc): self._set(exc=exc)

    def is_set(self): return self._event.isSet()
    def is_error(self): return self._exc is not None

    def get_error(self):
        assertions.fail_unless(self.is_error())
        return self._exc

    def get(self):
        """NOTE: If get is called for a future that has attached observers, then order is not guaranteed between them. 
                 i.e. get() may return before observers are called (or while they are running)
                 Also note that if future was set with an error, get will re-throw the exception in the caller's thread.
        """
        self._event.wait()
        assertions.fail_unless(self.is_set())
        if self.is_error():
            raise self._exc
        return self._val

    @staticmethod
    def preset(val):
        '''Convenience method, that returns a future that is preset with the value val.'''
        f = Future()
        f.set(val)
        return f

