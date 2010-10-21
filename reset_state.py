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
def reset_state(cls):

    def wrapped_init(self, *args, **kwds):
        original_init(self, *args, **kwds)
        original_values = {}
        for k in dir(self):
            if k[0:2] != "__":
                original_values[k] = getattr(self, k)
        self.__original_values = original_values
        
    def cls_reset_state(self):
        for (k, v) in self.__original_values.iteritems():
            setattr(self, k, v)
        
        for k in dir(self):
            if k[0:2] != "__" and k not in self.__original_values:
                delattr(self, k)

    original_init = cls.__init__
    cls.reset_state = cls_reset_state
    cls.__init__ = wrapped_init
    
    return cls
