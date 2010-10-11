"""\
Used in alert formatting. Allows administrators to set a format string that formats alerts 
nicely with all the parameters given by the program.
The added value over simple formatting is that if the administrator tries to use a parameter 
that isn't provided for that alert, it is handled gracefully, and also any parameters
that the administrator didn't specify in the format string are still shown, using a generic
format.

See the unit tests for more details on how this behaves.
"""
from UserDict import UserDict
import string

class FormattingProxy(dict):
    def st_items_retrieved(self):
        pass
    
    def __init__(self, data):
        self.update(data)
        self.st_items_retrieved = set()
        
    def __getitem__(self, key):
        
        if key in self:
            self.st_items_retrieved.add(key)
            return dict.__getitem__(self, key)
        else:
            return "<UNKNOWN PARAMETER " + str(key) + ">"
    
def format(fmt, **kwds):
    formatting_proxy = FormattingProxy(kwds)
    ret = fmt % formatting_proxy
    
    additional_arguments = set(kwds.iterkeys()).difference(formatting_proxy.st_items_retrieved)
    
    if (len(additional_arguments) > 0):
        return ret + "\nAdditional arguments:\n" + \
               "\n".join([(arg + " = " + str(kwds[arg])) for arg in sorted(additional_arguments)]) + "\n"
    else:
        return ret
           
    