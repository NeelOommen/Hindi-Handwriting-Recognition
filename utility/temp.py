import csv 

from unicode_list import test_set_labels

rows =[]

with open('D:\\GitHub\\Hindi-Handwriting-Recognition\\CNN_test_sandbox\\Dataset\\Local (Testing)\\annotations.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        rows.append(row)


for i in range(len(rows)):
    rows[i][1] = str(test_set_labels[rows[i][1]])

with open('D:\\GitHub\\Hindi-Handwriting-Recognition\\CNN_test_sandbox\\Dataset\\Local (Testing)\\annotations.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)