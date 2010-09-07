class NullObject(object):
    """See Python cookbook (2nd edition) receipe 6.17 - Implementing the Null Object Design Pattern"""
    def __new__(cls,*a,**kw):
        """Make it a singleton"""
        if '_inst' not in vars(cls):
            cls._inst = super(NullObject,cls).__new__(cls,*a,**kw)
        return cls._inst
    def __init__(self,*a,**kw): pass
    def __repr__(self): return "NullObject()"
    def __nonzero__(self): return False
    def __call__(self,*a,**kw): return self
    def __getattr__(self,name): return self
    def __setattr__(self,name,value): pass
    def __delattr__(self,name): pass
    def __len__(self): return 0
    def __iter__(self): return iter(())
    def __getitem__(self,i): return self
    def __setitem__(self,i,val): pass
    def __delitem__(self,i): pass
