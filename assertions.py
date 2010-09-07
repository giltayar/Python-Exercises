"""\
assertions - conveience class for conditional assertions/warnings
"""

import os
import exceptions
import logging
import traceback

class AssertionException(exceptions.Exception):
    pass

class Assertions(object):
    def __init__(self):
        """Logger may be set/get externally"""
        self.logger = logging.getLogger('Assertions') # will propagate to root logger unless overidden
        self._exit = os._exit # exit immediately, without cleanup
        self.b_fail_is_fatal = False # whether to throw exception or exit immediately on failure (for debugging)
        self.reset_events()
        
    def reset_events(self):
        self.had_assertion = False
        
    def _end_program(self):
        self.logger.critical('ENDING PROGRAM DUE TO ASSERTION!')
        self._exit(-1) 
    
    def _raise_exception(self,msg):
        raise AssertionException(msg)
        
    def fail(self,msg):
        if self.b_fail_is_fatal:
            self._end_program()
        self._raise_exception(msg)
    
    def msg(self, log_level, header, *a,**kw):
        self.had_assertion = True
        try:
            str_a = ', '.join(str(x) for x in a)
            str_kw = ', '.join(('%s=%s' % (k,v)) for k,v in kw.iteritems())
            str_info = 'INFO:%s KW:%s' % (str_a, str_kw)
        except:
            str_info = '(NO INFO - ERROR WHILE FORMATTING ARGS!)'
    
        stack_str = ''.join(traceback.format_stack())
        str_msg = '%s: %s\nStack:\n%s' % (header, str_info, stack_str)
        self.logger.log(log_level,str_msg)
        return str_msg
        
Assertions = Assertions()

##################################################

def fail(*a,**kw):
    msg = Assertions.msg(logging.ERROR, 'ASSERTION', *a,**kw)
    Assertions.fail(msg)

def fail_if(cond,*a,**kw):
    if cond:
        fail(*a,**kw)
    
def fail_unless(cond,*a,**kw):
    if not cond:
        fail(*a,**kw)
        
def warn(*a,**kw):
    Assertions.msg(logging.WARNING, 'WARNING',*a,**kw)

def warn_if(cond,*a,**kw):
    if cond:
        warn(*a,**kw)
    
def warn_unless(cond,*a,**kw):
    if not cond:
        warn(*a,**kw)

