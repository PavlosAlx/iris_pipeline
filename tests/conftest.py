import os, sys

HERE = os.path.dirname(__file__)         
SRC  = os.path.abspath(os.path.join(HERE, os.pardir, "src"))

sys.path.insert(0, SRC)
