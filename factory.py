"""\
A generic factory that creates objects for "roles" with registered creation functions.

>> f = Factory()
>> f.register('A',MyA) # MyA is a class that implements interface A
>> ...
>> a = f.create('A',1,2,x=3) # create object of role 'A' and pass the other arguments to it's constructor
"""
