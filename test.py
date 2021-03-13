import sys,os
sys.path.append(os.path.abspath(os.path.join(sys.path[0], 'utils')))
sys.path.append(os.path.abspath(os.path.join(sys.path[0], 'db_helper')))
sys.path.append('../')
print(sys.path)
from mongo_helper import *
from utils import *