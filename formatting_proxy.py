"""\
Used in alert formatting. Allows administrators to set a format string that formats alerts 
nicely with all the parameters given by the program.
The added value over simple formatting is that if the administrator tries to use a parameter 
that isn't provided for that alert, it is handled gracefully, and also any parameters
that the administrator didn't specify in the format string are still shown, using a generic
format.

See the unit tests for more details on how this behaves.
"""

class FormattingProxy(object):
    def __init__(self,dct):
        self.dct = dct
        self.st_items_retrieved = set()
        
    def __getitem__(self,key):
        if key in self.dct:
            self.st_items_retrieved.add(key)
            return self.dct[key]
        else:
            return "<UNKNOWN PARAMETER %s>" % (key,)
        
def format(format_string,**kw):
    fp = FormattingProxy(kw)
    text = format_string % fp
    
    lst_additional = []
    for name in sorted(kw.keys()):
        value = kw[name]
        if name not in fp.st_items_retrieved:
            lst_additional.append("%s = %s" % (name,value))    
    
    if lst_additional:
        text += """
Additional arguments:
%s
""" % '\n'.join(lst_additional)
        
    return text
    
        