import unittest
import add_parent_path # PyFlakesIgnore

from formatting_proxy import FormattingProxy, format

class TestFormattingProxy(unittest.TestCase):
    def test_sanity(self):
        dct = {'x':1, 'y':2}
        fp = FormattingProxy(dct)
        x = fp['x']
        self.assertEqual(x,1)
        self.assertEqual(fp.st_items_retrieved, set(['x']))
        
    def test_unknown(self):
        dct = {'x':1, 'y':2}
        fp = FormattingProxy(dct)
        nosuch = fp['nosuch']
        self.assertEqual(nosuch,"<UNKNOWN PARAMETER nosuch>")
        x = fp['x']
        self.assertEqual(x,1)
        self.assertEqual(fp.st_items_retrieved, set(['x']))

class TestFormat(unittest.TestCase):
    def test_all_used(self):
        fmt = """\
The value of x is %(x)s.
And y is %(y)s!
"""        
        text = format(fmt,x=3,y=5)
        self.assertEqual(text,"""\
The value of x is 3.
And y is 5!
""")        

    def test_not_all_used(self):
        fmt = "The value of x is %(x)s"
        text = format(fmt,x=3,y=5)
        self.assertEqual(text,"""\
The value of x is 3
Additional arguments:
y = 5
""")        
        
    def test_unknown(self):
        fmt = "The value of x is %(z)s"
        text = format(fmt,x=3,y=5)
        self.assertEqual(text,"""\
The value of x is <UNKNOWN PARAMETER z>
Additional arguments:
x = 3
y = 5
""")        
        
if __name__ == '__main__':
    unittest.main()
