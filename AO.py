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

from dynamic_proxy import DynamicProxy
from future import Future

import threading
import Queue

class AO(DynamicProxy):
    
    def __init__(self, obj, n_threads = 1, parent_ao = None):
        DynamicProxy.__init__(self)
        self.obj = obj
        if (parent_ao == None):
            self.method_dispatch_queue = Queue.Queue()
            self.threads = [threading.Thread(None, self.run) for i in xrange(n_threads)]
        else:
            self.method_dispatch_queue = parent_ao.method_dispatch_queue
        
    def start(self):
        if hasattr(self.obj, 'start'):
            self.obj.start()
        for thread in self.threads:
            thread.start()
    
    def run(self):
        while True:
            method_dispatch = self.method_dispatch_queue.get()
            if method_dispatch == 'done':
                break
            self.dispatch_method(method_dispatch)
            self.method_dispatch_queue.task_done()
            
    def dispatch_method(self, method_dispatch):
        
        try:
            method = getattr(method_dispatch['obj'], method_dispatch['name'])
        
            method_dispatch['future'].set(method(*method_dispatch['args'], **method_dispatch['kwds']))
            
        except Exception as exception:
            method_dispatch['future'].set_error(exception)
    
    def quit(self):
        for thread in self.threads:
            self.method_dispatch_queue.put('done')
        
        for thread in self.threads:
            thread.join()
            
        if hasattr(self.obj, 'quit'):
            self.obj.quit()
        
    def _dispatch(self, name, *args, **kwds):
        future = Future()
        
        self.method_dispatch_queue.put({'obj': self.obj, 'name': name, 'args': args, 'kwds': kwds, 'future': future});
        
        return future
    
    def __str__(self):
        return "%s(%s)" % (self.__class__.__name__, self.obj.__class__.__name__)
        
class SatelliteAO(AO):
    def __init__(self, obj, parent_ao):
        AO.__init__(self, obj, 1, parent_ao)
        
    def start(self):
        pass

    def quit(self):
        raise Exception("Not allowed in satellite active objects")
        