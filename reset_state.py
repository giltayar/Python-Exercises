"""\
reset_state - a class decorator that lets you return the instance to its state as it was 
just after construction.

>> @reset_state
>> class X(object):
>>    ...
>> ...
>> x = X(...)
>> ... # use x. change its state
>> x.reset_state() # this method was added by the decorator. calling it returns x to original state

NOTE: Requires that class X's members can be deep copied (using copy.deepcopy)
"""

import copy

def reset_state(C):
    orig_init = C.__init__
    def new_init(self,*a,**kw):
        orig_init(self,*a,**kw)
        self.__orig_state = copy.deepcopy(self.__dict__)
    C.__init__ = new_init
    
    def _reset_state(self):
        self.__dict__ = copy.deepcopy(self.__orig_state)
    C.reset_state = _reset_state
    
    return C
    