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
class Future(object):

    def __init__(self):
        self._get_event = threading.Event()
        self._observers = []

    def get(self):
        self._get_event.wait()
        return self._value
    
    def set(self, value):
        self._value = value
        self._get_event.set()
        for observer in self._observers:
            observer(self)
        
    def is_set(self):
        return self._get_event.is_set()

    def attach_observer(self, observer):
        self._observers.append(observer)
        if self.is_set():
            observer(self)
        
        