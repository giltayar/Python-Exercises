def with_index(itr):
    """This is the same as builtin function enumerate. Don't use this except as an exercise.
       I changed the name, because I don't like overriding builtin names.
       
       Produces an iterable which returns pairs (i,x) where x is the value of the original,
       and i is it's index in the iteration, starting from 0.
    """
    i = 0
    for value in itr:
        yield (i, value)
        i += 1
    
        
def fibonacci():
    """An infinite generator for the fibonacci series, where:
       Fib[0] = 0
       Fib[1] = 1
       Fib[n+2] = Fib[n] + Fib[n+1]
    """
    f1 = 0
    yield f1
    f2 = 1
    yield f2
    while True:
        f3 = f1 + f2
        yield f3
        f1 = f2
        f2 = f3
        

def product(*seqs):
    """Same as itertools.product - Don't use this except as an exercise.
       Returns a generator for the cartesian product of all sequences given as input. 
       If called with N sequences, then each returned item is a list of N items - one from each sequence.
       For example, product([1,2,3],'ABC',[True,False]) produces the following items:
           [1,'A',True]
           [1,'A',False]
           [1,'B',True]
           ...
       
       See my blog for discussion of this implementation: 
       http://www.ronnie-midnight-oil.net/2008/05/ok.html
    """
    ret = [[]]
    for seq in seqs:
        ret = [ret_seq + [s] for ret_seq in ret for s in seq]
            
    for value in ret:
        yield value