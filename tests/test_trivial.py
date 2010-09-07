import unittest
import add_parent_path # PyFlakesIgnore

from trivial import Adder

class TestTrivial(unittest.TestCase):
    def test_sanity(self):
        adder = Adder(3)
        sum = adder.add(10)
        self.assertEqual(sum,13)
        
if __name__ == '__main__':
    unittest.main()
