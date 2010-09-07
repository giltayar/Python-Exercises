import unittest
import add_parent_path # PyFlakesIgnore

from cache import cache

class TestCache(unittest.TestCase):
    def setUp(self):
        class A(object):
            def __init__(self):
                self.n_calls = 0
            
            @cache
            def add(self,x,y):
                self.n_calls += 1
                return x+y

            @cache
            def sub(self,x,y):
                self.n_calls += 1
                return x-y

            @cache
            def echo(self,x):
                self.n_calls += 1
                return x
                
        self.a = A()
                
    def test_sanity(self):        
        # first call not in cache
        sum = self.a.add(2,3)
        self.assertEqual(sum,5)
        self.assertEqual(self.a.n_calls,1)
        
        # second call already in cache
        sum = self.a.add(2,3)
        self.assertEqual(sum,5)        
        self.assertEqual(self.a.n_calls,1)
        
        # call with different args - not in cache
        sum = self.a.add(2,4)
        self.assertEqual(sum,6)
        self.assertEqual(self.a.n_calls,2)

        # call both sets of args again - both should still be in cache
        sum = self.a.add(2,3)
        self.assertEqual(sum,5)
        sum = self.a.add(2,4)
        self.assertEqual(sum,6)
        self.assertEqual(self.a.n_calls,2)

    def test_separate_caches(self):
        # prime cache for add() and verify it
        sum = self.a.add(2,3)
        self.assertEqual(sum,5)
        self.assertEqual(self.a.n_calls,1)
        sum = self.a.add(2,3)
        self.assertEqual(sum,5)
        self.assertEqual(self.a.n_calls,1)
        
        # verify cache for sub() is different and also works
        diff = self.a.sub(2,3)
        self.assertEqual(diff,-1)
        self.assertEqual(self.a.n_calls,2)
        diff = self.a.sub(2,3)
        self.assertEqual(diff,-1)
        self.assertEqual(self.a.n_calls,2)
        
    def test_kwargs(self):
        # first call
        diff = self.a.sub(x=3,y=2)
        self.assertEqual(diff,1)
        self.assertEqual(self.a.n_calls,1)

        # another call with same kwargs uses cache
        diff = self.a.sub(x=3,y=2)
        self.assertEqual(diff,1)
        self.assertEqual(self.a.n_calls,1)
        
        # call with different order also uses cache
        diff = self.a.sub(y=2,x=3)
        self.assertEqual(diff,1)
        self.assertEqual(self.a.n_calls,1)
        
        # call with different args/kwargs mix is considered different call
        diff = self.a.sub(3, y=2)
        self.assertEqual(diff,1)
        self.assertEqual(self.a.n_calls,2)
        
        # another call to this variant now uses cache
        diff = self.a.sub(3, y=2)
        self.assertEqual(diff,1)
        self.assertEqual(self.a.n_calls,2)
        
    def test_none(self):
        # baseline - echo simple integer
        x = self.a.echo(3)
        self.assertEqual(x,3)
        self.assertEqual(self.a.n_calls,1)
        x = self.a.echo(3)
        self.assertEqual(x,3)
        self.assertEqual(self.a.n_calls,1)

        # check with None
        x = self.a.echo(None)
        self.assertEqual(x,None)
        self.assertEqual(self.a.n_calls,2)
        x = self.a.echo(None)
        self.assertEqual(x,None)
        self.assertEqual(self.a.n_calls,2)

    def test_dct(self):
        # limitation - doesn't work with arguments that aren't hashable
        d = {1:2}
        self.assertRaises(TypeError,self.a.echo,d)
        
if __name__ == '__main__':
    unittest.main()
