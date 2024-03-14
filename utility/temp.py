import sys

sys.path.insert(0,'../Hindi-Handwriting-Recognition/')

import os
from os import listdir

path = 'CNN_test_sandbox\Dataset\Train'

with open('dump.txt', 'w') as f:
    paths = listdir(path)
    for line in paths:
        f.write(line)
        f.write('\n')