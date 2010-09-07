import unittest
import add_parent_path # PyFlakesIgnore

from retry import retry

class TestRetry(unittest.TestCase):
    def _get_test_obj(self,max_retries,n_fail):
        class A(object):
            def __init__(self):
                self.n_calls = 0
            
            @retry(max_retries)
            def add(self,x,y):
                self.n_calls += 1
                if self.n_calls <= n_fail:
                    raise Exception('oops')
                return x+y
        return A()
                
    def test_sanity(self):
        # check call with no failures
        a = self._get_test_obj(max_retries=5,n_fail=0)
        sum = a.add(2,3)
        self.assertEqual(sum,5)
        self.assertEqual(a.n_calls,1)
        
        # check call the succeeds after retries
        a = self._get_test_obj(max_retries=5,n_fail=2)
        sum = a.add(2,3)
        self.assertEqual(sum,5)
        self.assertEqual(a.n_calls,3)

    def test_max_retries(self):
        # check max_retries == n_fail
        a = self._get_test_obj(max_retries=3,n_fail=3)
        self.assertRaises(Exception,a.add,2,3)
        self.assertEqual(a.n_calls,3)

        # check max_retries < n_fail
        a = self._get_test_obj(max_retries=2,n_fail=3)
        self.assertRaises(Exception,a.add,2,3)
        self.assertEqual(a.n_calls,2)

        # check max_retries == n_fail+1 (just barely made it)
        a = self._get_test_obj(max_retries=4,n_fail=3)
        sum = a.add(2,3)
        self.assertEqual(sum,5)
        self.assertEqual(a.n_calls,4)
        
if __name__ == '__main__':
    unittest.main()
