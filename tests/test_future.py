import unittest
import add_parent_path # PyFlakesIgnore
import threading
import assertions
import future

import exceptions
class TestException(exceptions.Exception):
    pass

class Result(object):
    def __init__(self):
        self.val = None

class TestFuture(unittest.TestCase):
    def setUp(self):
        assertions.Assertions.reset_events()
        self.result = Result()

    def tearDown(self):
        self.failIf(assertions.Assertions.had_assertion)
                
    def test_normal(self):
        f = future.Future()
        self.failIf(f.is_set())
        
        threading.Thread(target=f.set,args=[3]).start()
        val = f.get()
        self.failUnless(f.is_set())
        self.assertEqual(val,3)

    def test_set_none(self):
        f = future.Future()
        f.set(None)
        val = f.get()
        self.failUnless(f.is_set())
        self.assertEqual(val,None)

    def test_preset(self):
        f = future.Future.preset('james')
        self.failUnless(f.is_set())
        val = f.get()
        self.assertEqual(val,'james')

    def test_observers(self):
        f = future.Future()

        def observer(the_future):
            self.assert_(the_future.is_set())
            self.assertEqual(self.result.val,None)
            self.result.val = (the_future.get(),id(threading.currentThread()))

        f.attach_observer(observer)
        t = threading.Thread(target=f.set,args=['a name'])
        t.start()
        t.join()
        self.failUnless(f.is_set())
        self.assertEqual(self.result.val, ('a name', id(t)))
        
        self.result.val = None
        f.attach_observer(observer) # attaching observer after future is set calls observer immediately (from our thread)
        self.assertEqual(self.result.val, ('a name', id(threading.currentThread())))

    def test_set_error(self):
        f = future.Future()
        threading.Thread(target=f.set_error,args=[TestException('BAD')]).start()
        self.assertRaises(TestException,f.get)
        self.failUnless(f.is_set())
        self.failUnless(f.is_error())
        self.assertEqual(str(f.get_error()),'BAD')        
                
if __name__ == '__main__':
    unittest.main()
