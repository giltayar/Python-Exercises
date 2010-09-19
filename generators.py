def with_index(itr):
    """This is the same as builtin function enumerate. Don't use this except as an exercise.
       I changed the name, because I don't like overriding builtin names.
       
       Produces an iterable which returns pairs (i,x) where x is the value of the original,
       and i is it's index in the iteration, starting from 0.
    """
    i = 0
    for x in itr:
        yield i,x
        i += 1
        
def fibonacci():
    """An infinite generator for the fibonacci series, where:
       Fib[0] = 0
       Fib[1] = 1
       Fib[n+2] = Fib[n] + Fib[n+1]
    """
    a,b = 0,1
    yield a
    yield b
    while True:
        a,b = b,a+b
        yield b

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
    def prod2(A,b): return (a+[x] for a in A for x in b)
    return reduce(prod2,seqs,[[]])
