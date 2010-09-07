import unittest
import add_parent_path  # PyFlakesIgnore

import assertions
from itertools import product
from assert_testing_helper import AssertTestingHelper

class TestAssertions(unittest.TestCase):
    def setUp(self):
        self.helper = AssertTestingHelper()
        self.helper.install_hooks()
        assertions.Assertions.reset_events()
    
    def tearDown(self):
        self.helper.uninstall_hooks()
                
    def test_fail(self):
        self.assertRaises(assertions.AssertionException,assertions.fail)
        s = self.helper.get_output()
        self.assert_(s.startswith("ASSERTION: INFO: KW:\nStack:\n"),s)
        self.assertEquals(assertions.Assertions.had_assertion,True)

    def test_warn(self):
        assertions.warn(3,name='john')
        s = self.helper.get_output()
        self.assert_(s.startswith("WARNING: INFO:3 KW:name=john\nStack:\n"),s)
        self.assertEquals(assertions.Assertions.had_assertion,True)
        
    def test_bad_format(self):
        class BadStr(object):
            def __repr__(self):
                raise Exception,"can't format this object to string"
        assertions.warn(bad=BadStr())
        s = self.helper.get_output()
        start = "WARNING: (NO INFO - ERROR WHILE FORMATTING ARGS!)"
        self.assert_(s.startswith(start),'s=%s'%s)
           
    def test_conditional(self):
        for base,variant,meet_condition in product(['fail','warn'],['if','unless'],[True,False]):
            fname = base + '_' + variant
            f = getattr(assertions, fname)
            
            if variant == 'if':
                cond_param = meet_condition
            else:
                cond_param = not meet_condition
            
            # run the method
            had_test_exception = False
            try:
                f(cond_param,3,'jane')
            except assertions.AssertionException:
                had_test_exception = True
            s = self.helper.get_output()
                
            # check result
            which_test = 'base=%s, variant=%s, do_fail=%s' % (base,variant,meet_condition)
            if meet_condition: # assertion/warning triggered
                if base == 'fail':
                    self.assert_(had_test_exception,which_test)
                if base == 'fail':
                    header = "ASSERTION"
                else:
                    header = "WARNING"
                start = "%s: INFO:3, jane KW:\nStack:\n" % header
                self.assert_(s.startswith(start),'%s\nstart=%s\ns=%s' % (which_test,start,s))
            else:
                self.failIf(s,'assertion/warning should not have happened. %s' % which_test)
                
if __name__ == '__main__':
    unittest.main()
