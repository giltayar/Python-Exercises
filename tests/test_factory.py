import unittest
import add_parent_path # PyFlakesIgnore

from factory import Factory


class TestFactory(unittest.TestCase):
    def test_sanity(self):
        class A(object): pass
        class B(object):
            def __init__(self,x,y):
                self.x = x
                self.y = y
        class B2(object):
            """B2 is a replacement for B, but accepts a third parameter z.
               clients that use the factory will expect a class that has only x and y
            """
            def __init__(self,x,y,z):
                self.x = x
                self.y = y
                self.z = z
        
        f = Factory()
        f.register('A',A)
        f.register('B',B)
        a = f.create('A')

        self.assertEqual(type(a),A)
        b = f.create('B',1,y=3)
        self.assertEqual(type(b),B)
        self.assertEqual(b.x,1)
        self.assertEqual(b.y,3)
        
        def create_B2(x,y): return B2(x,y,z='zzz')
        f.register('B',create_B2)
        b = f.create('B',1,y=3)
        self.assertEqual(b.x,1)
        self.assertEqual(b.y,3)
        self.assertEqual(b.z,'zzz')
                
if __name__ == '__main__':
    unittest.main()
