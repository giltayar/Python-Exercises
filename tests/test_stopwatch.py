import unittest
import add_parent_path # PyFlakesIgnore
import time

from stopwatch import Stopwatch

class TestStopwatch(unittest.TestCase):
    def test_sanity(self):
        s = Stopwatch()
        time.sleep(0.5)
        duration = s.duration()
        self.assert_(0.45 < duration < 0.55, 'duration=%s' % duration)
    
if __name__ == '__main__':
    unittest.main()
