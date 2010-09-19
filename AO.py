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

import logging
import traceback
import threading
import Queue
import assertions
from dynamic_proxy import DynamicProxy
from future import Future
from null_object import NullObject

class AOException(Exception):
    pass

def no_trace(f):
    '''decorator which marks f, so we don't trace calls to it'''
    f.no_trace = 1
    return f
        
class BaseAO(DynamicProxy):
    '''Base logic for active object that is shared between different implementations such as normal AO and
       SatelliteAO.
    '''
    def __init__(self,passive_obj):
        DynamicProxy.__init__(self)
        self.obj = passive_obj
        self.obj._ao = self # allow passive object to make async calls to itself (and be aware of AO in general)

        if hasattr(self.obj,'logger'):
            self.logger = logging.getLogger(self.obj.logger.name + '.AO')
        else:
            self.logger = NullObject()
            self.logger.warning('%s - No logger found for passive object' % self)
        
    def __str__(self):
        return "%s(%s)" % (type(self).__name__, type(self.obj).__name__)
        
    def start(self):
        self.logger.info("AO started")

        # If self.obj has start method, call it
        try:
            obj_start = self.obj.start
            if callable(obj_start):
                try:
                    obj_start()
                except Exception, e:
                    self.logger.error('Got exception while starting AO. %s' % traceback.format_exc(e))
        except AttributeError:
            pass # no start method

    def quit(self):
        self.logger.info("AO stopped (quit called)")

        # If self.obj has quit method, call it
        try:
            obj_quit = self.obj.quit
            if callable(obj_quit):
                try:
                    obj_quit()
                except Exception, e:
                    self.logger.error('Got exception while quitting AO. %s' % traceback.format_exc(e))
        except AttributeError:
            pass # no quit method        
        self.logger.debug('user quit hook finished')
        
    def _dispatch(self,name,*a,**kw):
        f = Future()
        cmd = BaseAO.Cmd(f,self,name,a,kw)
        self.enq(cmd)
        return f
        
    class Cmd(object):
        def __init__(self,future,ao,attr,a,kw):
            self.future = future
            self.ao = ao
            self.attr = attr
            self.a = a
            self.kw = kw
        def __str__(self):
            return "Cmd(ao=%s, attr=%s, a=%s, kw=%s)" % (self.ao,self.attr,self.a,self.kw)
        def __call__(self):
            mth = getattr(self.ao.obj,self.attr)
            b_trace = not hasattr(mth,'no_trace')
            if b_trace:
                self.ao.logger.debug('ENTERing %s, cmd=%s' % (self.attr,self))
            try:
                rv = mth(*self.a,**self.kw) # execute the method
                if b_trace:
                    self.ao.logger.debug('EXITed %s, cmd=%s' % (self.attr,self))
                self.future.set(rv)
            except Exception, e:
                self.ao.logger.error('EXITed %s with Exception. %s, cmd=%s' % (self.attr,traceback.format_exc(e),self))
                self.future.set_error(e)

class AO(BaseAO):
    '''A standard AO with one or more threads of execution'''
    def __init__(self,passive_obj,n_threads=1):
        BaseAO.__init__(self,passive_obj)
        self.q = Queue.Queue()
        self.n_threads = n_threads
        self.threads = []
        
    def start(self):
        BaseAO.start(self)
        
        # start the threads
        for i in xrange(self.n_threads):
            name = 'AO_%s_%s' % (type(self.obj).__name__,i+1)
            t = threading.Thread(target=self._run, name=name)
            self.threads.append(t)
            t.start()

    def _run(self):
        while True:
            cmd = self.q.get()
            try:
                rc = cmd()
                if rc:
                    break
            except Exception, e:
                self.logger.error('Uncaught Exception. details in next log') # extra paranoid since this is last line of defense
                assertions.warning('Uncaught Exception details',ao=self, details=traceback.format_exc(e))

    def enq(self,cmd):
        self.q.put(cmd)
            
    def quit(self):
        BaseAO.quit(self)
        def finish(): return 1
        for i in range(self.n_threads):
            self.enq(finish)
        for t in self.threads:
            self.logger.debug('waiting for thread %s' % (id(t),))
            t.join()
        self.logger.debug('quit finished')

class SatelliteAO(BaseAO):
    '''An AO which doesn't have any threads, but instead uses the threads and command queues of a parent AO.
       Note that the parent_ao may itself be a SatelliteAO, in which case the command is enqued to its parent, 
       and so on.
    '''
    def __init__(self,passive_obj,parent_ao):
        BaseAO.__init__(self,passive_obj)
        self.parent_ao = parent_ao
        
    def enq(self,cmd):
        self.parent_ao.enq(cmd)
        
