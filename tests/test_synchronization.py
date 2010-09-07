import unittest
import add_parent_path # PyFlakesIgnore

import threading
import time

from synchronization import synchronize_using, synchronized
from stopwatch import Stopwatch

class TestSynchronizeUsing(unittest.TestCase):
    def test_sanity(self):
        lock1 = threading.RLock()
        lock2 = threading.RLock()
        
        def sleep_and_inc(lock,sleep_time): 
            with synchronize_using(lock):
                time.sleep(sleep_time)
                lock.sync_test_counter = getattr(lock,'sync_test_counter',0) + 1
                
        sleep_time = 0.5
        n = 4
        
        s = Stopwatch()
        lst_threads = []
        for lock in [lock1,lock2]:
            for _ in xrange(n):
                t = threading.Thread(target=sleep_and_inc,args=[lock,sleep_time])
                lst_threads.append(t)
                t.start()

        # wait for all threads, then check results
        for t in lst_threads:
            t.join()
            
        duration = s.duration()
        self.assertEqual(lock1.sync_test_counter,n)
        self.assertEqual(lock2.sync_test_counter,n)
        ideal_time = n*sleep_time
        self.assert_(ideal_time*0.9 < duration < ideal_time*1.1, "duration=%s, ideal=%s" % (duration,ideal_time))
        

class TestSynchronized(unittest.TestCase):
    def setUp(self):
        class Synched(object):
            def __init__(self,sleep_time):
                self._lock = threading.RLock() # used by @synchronized decorator
                self.sleep_time = sleep_time
                self.x = 0

            def add(self,y):
                tmp = self.x
                time.sleep(self.sleep_time)
                self.x += y
                return tmp

            @synchronized
            def sync_add(self,y):
                return self.add(y)

        self.s = Synched(1)
        
    def test_normal(self):
        stopwatch = Stopwatch()
        threading.Thread(target=self.s.sync_add,args=[10]).start()
        time.sleep(0.05) # make sure other thread gets head start (and the mutex)
        val = self.s.sync_add(5)
        self.assertEqual(val,10)
        
        duration = stopwatch.duration()
        self.assert_(duration > 1.9*self.s.sleep_time, 'calls completed too quickly. duration=%s' % duration)

    def test_no_sync(self):
        stopwatch = Stopwatch()
        threading.Thread(target=self.s.add,args=[10]).start()
        time.sleep(0.05) # make sure other thread gets head start
        val = self.s.add(5)
        self.assertEqual(val,0)
        
        duration = stopwatch.duration()
        self.assert_(duration < 1.2*self.s.sleep_time, 'calls took too long. duration=%s' % duration)
        
if __name__ == '__main__':
    unittest.main()
