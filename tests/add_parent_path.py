import sys
from os.path import join,abspath,dirname

this_dir = dirname(__file__)
parent_dir = abspath(join(this_dir,r'..'))

if parent_dir not in sys.path:
    sys.path.append(parent_dir)
