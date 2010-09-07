import unittest
import add_parent_path # PyFlakesIgnore

from dynamic_proxy import DynamicProxy

class TestDynamicProxy(unittest.TestCase):
    def test_sanity(self):
        class MyProxy(DynamicProxy):
            def __init__(self,x):
                super(MyProxy,self).__init__()
                self.x = x
            def _dispatch(self,method_name,*a,**kw):
                return 'x=%s, method_name=%s, a=%s, kw=%s' % (self.x,method_name,a,kw)

        p = MyProxy(666)
        s = p.foo(1,True,y='Jim')
        self.assertEqual(s,"x=666, method_name=foo, a=(1, True), kw={'y': 'Jim'}")

if __name__ == '__main__':
    unittest.main()
