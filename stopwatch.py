"""\
Stopwatch - a convenience class for timing things.

>> s = Stopwatch()
>> ... # do something you want timed
>> duration = s.duration()
"""

from datetime import datetime

class Stopwatch(object):
    def __init__(self):
        self.start()
        
    def start(self):
        self._start = datetime.now()
        
    def duration(self):
        d = datetime.now() - self._start
        return d.seconds + float(d.microseconds) / 10**6
