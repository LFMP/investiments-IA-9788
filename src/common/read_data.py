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
            data[filename[:-14]] = {}
            for (index, row) in enumerate(spamreader):
                if(index == 0):
                    header = row
                    for column_name in header:
                        data[filename[:-14]][column_name] = []
                else:
                    for (i, value) in enumerate(row):
                        if (i != 0):
                            data[filename[:-14]][header[i]].append(float(value))
                        else:
                            data[filename[:-14]][header[i]].append(value)
        for name in header:
            data[filename[:-14]][name] = np.array(
                data[filename[:-14]][name]).flatten()
    return data

def read_data2016():
    companys_files = [x for x in os.listdir(os.getcwd() + '/src/database/2016_database/')]
    # companys = [x.split('.')[0] for x in companys_files if '.csv' in x]
    companys_2016_files = [x for x in companys_files if '.csv' in x]

    data = {}
    header = []
    for filename in companys_2016_files:
        path = os.getcwd() + '/src/database/2016_database/' + filename
        with open(path, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            data[filename[:-4]] = {}
            for (index, row) in enumerate(spamreader):
                if(index == 0):
                    header = row
                    for column_name in header:
                        data[filename[:-4]][column_name] = []
                else:
                    for (i, value) in enumerate(row):
                        if i == 0:
                            data[filename[:-4]][header[i]].append(value)
                        elif i in range(1,6):
                            data[filename[:-4]][header[i]].append(float(value))
                        else:
                            data[filename[:-4]][header[i]].append(int(value))
    return data
