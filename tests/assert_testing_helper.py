import add_parent_path # PyFlakesIgnore
import copy
import logging
import assertions
from StringIO import StringIO

class AssertTestingHelper(object):
    def __init__(self,b_raise_exception=True):
        self.b_raise_exception = b_raise_exception
        
    def install_hooks(self):
        self._orig_assert_logger = assertions.Assertions.logger

        # install a logger for assertions module that catches logs in StringWriter self.output
        logger = logging.getLogger('TestAssertions')
        logger.propagate = False
        logger.setLevel(logging.WARNING) # assertions should not log below this level    

        # remove previous loggers, since we may be getting a logger from previous invocations
        for h in copy.copy(logger.handlers): # safer to copy list, since we modify it during iteration
            logger.removeHandler(h)

        self.output = StringIO()
        handler = logging.StreamHandler(self.output)
        logger.addHandler(handler)
        
        assertions.Assertions.logger = logger
        
    def uninstall_hooks(self):
        assertions.Assertions.logger = self._orig_assert_logger

    def get_output(self, b_reset=True):
        s = self.output.getvalue()
        if b_reset:
            self.output.seek(0)
            self.output.truncate()
        return s
        