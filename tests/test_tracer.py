import unittest
import add_parent_path # PyFlakesIgnore

from tracer import Tracer

class TestTracer(unittest.TestCase):
    def setUp(self):
        class Logger(object):
            def __init__(self):
                self.lines = []
            def __call__(self,msg):
                self.lines.append(msg)
            
        self.logger = Logger()
        
    def test_sanity(self):
        class A(object):
            def __init__(self,x):
                self.x = x                
            def foo(self,y):
                return self.x+y
            def bar(self):
                return 'bar!'

        tracer = Tracer(A(10),self.logger)
        x = tracer.foo(3)
        self.assertEqual(x,13)
        self.assertEqual(self.logger.lines,[
            "foo called with a=(3,), kw={}",
            "foo returned 13",
        ])

        x = tracer.bar()
        self.assertEqual(x,'bar!')
        self.assertEqual(self.logger.lines[2:],[
            "bar called with a=(), kw={}",
            "bar returned bar!",
        ])
        
if __name__ == '__main__':
    unittest.main()
