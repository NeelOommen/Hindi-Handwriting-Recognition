import sys

sys.path.insert(0, '../Hindi-Handwriting-Recognition/')

from utility.dataset_initializer import createCSV

path_to_dataset = 'D:\GitHub\Hindi-Handwriting-Recognition\CNN_test_sandbox\Dataset\Train'

createCSV(path_to_dataset)