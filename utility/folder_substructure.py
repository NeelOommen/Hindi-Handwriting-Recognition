import os

from unicode_list import hindi_unicode_characters

for i in hindi_unicode_characters:
    os.mkdir(os.path.join('..\Hindi-Handwriting-Recognition\Dataset', i))
    #print(i)

print('Folders Created')