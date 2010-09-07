import unittest
import add_parent_path  # PyFlakesIgnore
import logging
import threading
import time
from stopwatch import Stopwatch
from synchronization import synchronized

from assert_testing_helper import AssertTestingHelper

import AO

class TestAO(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger("TestAO")
        self.logger.debug("setUp started")
        
        # break connection between default logger and root logger, to silence it up
        self.default_logger = logging.getLogger('AO')

        self.assert_helper = AssertTestingHelper(b_raise_exception=False)
        self.assert_helper.install_hooks()
        self.aos_to_stop = []
        
    def tearDown(self):
        self.logger.debug("tearDown started")
        self.default_logger.propagate = True
            
        self.assert_helper.uninstall_hooks()
        for ao in self.aos_to_stop:
            ao.quit()
        self.logger.debug("tearDown finished")
        
    def test_sanity(self):
        class A(object):
            def __init__(self,name):
                self.name = name
            def repeat(self,n,msg):
                return '%s: %s' % (self.name, ', '.join(n*[msg]))
            def get_thread(self):
                return id(threading.currentThread())
        ao = AO.AO(A('bob'))
        ao.start()
        self.aos_to_stop.append(ao)
        
        val = ao.repeat(3,msg='hi').get()
        self.assertEqual(val,'bob: hi, hi, hi')
        
        self.assertEqual(str(ao),'AO(A)')
        
        t_id = ao.get_thread().get()
        self.assertNotEqual(t_id, id(threading.currentThread()))

    def test_passive_object_hooks(self):
        class Passive(object):
            def start(self):
                self.ao_id = id(self._ao)
            def quit(self):
                self.b_quit = True
        
        p = Passive()        
        ao = AO.AO(p)
        ao.start()
        self.aos_to_stop.append(ao)
        
        self.assertEqual(p.ao_id,id(ao))
        ao.quit()
        self.assertEqual(p.b_quit,True)
        
    def test_n_threads(self):
        sleep_time = 0.1
        
        class Sleeper(object):
            def __init__(self):
                self._lock = threading.RLock() # used by @synchronized decorator
                self.i = 0
                self.thread_ids = set()
                
            @synchronized
            def _critical_section(self):
                self.thread_ids.add(id(threading.currentThread()))
                self.i += 1
                            
            def sleep(self):
                time.sleep(sleep_time)
                self._critical_section()
        
        n_threads = 5
        n_calls = 20
        ao = AO.AO(Sleeper(),n_threads)
        ao.start()
        self.aos_to_stop.append(ao)
        
        s = Stopwatch()
        futures = [ao.sleep() for i in xrange(n_calls)]
        for f in futures:
            f.get()
        duration = s.duration()
        expected = sleep_time*n_calls / float(n_threads)
        self.assert_(0.9*expected < duration < 1.2*expected, 'duration=%s, expected=%s' % (duration,expected))
        self.assertEqual(ao.obj.i,n_calls)
        self.assertEqual(len(ao.obj.thread_ids),n_threads)
        self.failIf(id(threading.currentThread()) in ao.obj.thread_ids)
        
    def test_satellite(self):
        class A(object):
            def get_ids(self):
                return id(self),id(threading.currentThread())
        ao = AO.AO(A())
        ao.start()
        self.aos_to_stop.append(ao)
        sat = AO.SatelliteAO(A(),ao)
        sat.start()
        a1, t1 = ao.get_ids().get()
        a2, t2 = sat.get_ids().get()
        self.assertEqual(t1,t2)
        self.assertNotEqual(a1,a2)
        
    def test_quit(self):
        class A(object):
            def get_thread(self):
                time.sleep(0.1) # keep thread busy, so we cycle through all of them
                return threading.currentThread()
        n_threads = 3
        ao = AO.AO(A(),n_threads)
        ao.start()
        
        futures = [ao.get_thread() for i in xrange(n_threads)]
        threads = [f.get() for f in futures]
        for t in threads:
            self.failUnless(t.isAlive())
        ao.quit()
        for t in threads:
            self.failIf(t.isAlive())
                
    def test_exception(self):
        class Bad(object):
            def bad(self):
                raise Exception, "I'm a bad class"
        ao = AO.AO(Bad())
        ao.start()
        self.aos_to_stop.append(ao)

        f = ao.bad()
        self.assertRaises(Exception,f.get)
        self.assertEquals(f.is_error(),True)
        self.assertEquals(str(f.get_error()),"I'm a bad class")
    
if __name__ == '__main__':
    unittest.main()
