"""A trivial class, used in the training as a sanity to see your setup is installed correctly.
"""

class Adder(object):
    def __init__(self,x):
        self.x = x
        
    def add(self,y):
        return y + self.x
