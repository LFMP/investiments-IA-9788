import csv
import os
import numpy as np


def read_data2mov():
    companys_files = [x for x in os.listdir(os.getcwd() + '/database/')]
    companys_14_15_files = [x for x in companys_files if '2014-2015' in x]

    data = {}
    header = []
    for filename in companys_14_15_files:
        path = os.getcwd() + '/database/' + filename
        with open(path, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            data[filename[:-8]] = {}
            for (index, row) in enumerate(spamreader):
                if(index == 0):
                    header = row
                    for column_name in header:
                        data[filename[:-8]][column_name] = []
                else:
                    for (i, value) in enumerate(row):
                        if (i != 0):
                            data[filename[:-8]][header[i]].append(float(value))
                        else:
                            data[filename[:-8]][header[i]].append(value)
        for name in header:
            data[filename[:-8]][name] = np.array(
                data[filename[:-8]][name]).flatten()

    return data
