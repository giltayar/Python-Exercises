import unittest
import add_parent_path # PyFlakesIgnore

from partial import partial

class TestPartial(unittest.TestCase):       
    def test_sanity(self):
        def foo(x,y,z): return 100*x + 10*y + z
        
        f = partial(foo) # don't bind anything
        self.assertEqual(f(1,2,z=3),foo(1,2,z=3))

        f = partial(foo,1)
        self.assertEqual(f(2,3),foo(1,2,3))
        
        f = partial(foo,1,z=3)
        self.assertEqual(f(2),foo(1,2,3))
                
if __name__ == '__main__':
    unittest.main()
