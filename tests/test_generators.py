import unittest
import add_parent_path # PyFlakesIgnore

from itertools import islice
from generators import with_index, fibonacci, product

class TestIndex(unittest.TestCase):
    def test_sanity(self):
        lst = list(with_index('bob'))
        self.assertEqual(lst,[
            (0,'b'),
            (1,'o'),
            (2,'b'),
        ])
        
class TestFibonacci(unittest.TestCase):
    def test_sanity(self):
        expected = [0,1,1,2,3,5,8,13,21]
        lst = list(islice(fibonacci(),len(expected)))
        self.assertEqual(lst,expected)
                
class TestProduct(unittest.TestCase):
    def test_empty(self):        
        self.assertEqual(list(product()),[[]])

    def test_single(self):        
        self.assertEqual(list(product([1,2,3])),[[1],[2],[3]])

    def test_double(self):        
        lst = list(product([1,2,3],'XY'))
        self.assertEqual(lst,[
            [1,'X'],
            [1,'Y'],
            [2,'X'],
            [2,'Y'],
            [3,'X'],
            [3,'Y'],
        ])

    def test_many(self):        
        lst = list(product([1,2,3],'XY',[True,False],['well','now']))
        self.assertEqual(len(lst),3*2*2*2)
        expected_start = [
            [1,'X',True,'well'],
            [1,'X',True,'now'],
            [1,'X',False,'well'],
            [1,'X',False,'now'],
            [1,'Y',True,'well'],
        ]
        self.assertEqual(lst[:len(expected_start)],expected_start)

        expected_end = [
            [3,'Y',True,'now'],
            [3,'Y',False,'well'],
            [3,'Y',False,'now'],
        ]
        self.assertEqual(lst[-len(expected_end):],expected_end)        
        
if __name__ == '__main__':
    unittest.main()
