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
