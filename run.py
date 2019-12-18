import sys
import os
from os import path
import importlib
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("contributor_folder")

get_data_reads = set()
merge_data_reads = set(['mta.census_income', 'mta.census_tracts', 'mta.neighborhoods', 'mta.population', 'mta.stations', 'mta.transportation_percentages', 'mta.q_train'])


def file_walk(subdir):
    algorithms = []
    for r,d,f in os.walk(subdir):
        if '__pycache__' in r:
            break
        for file in f:
            if 'Zip' in file:   continue
            if file.split(".")[-1] == "py" and file != '__init__.py':
                name_module = ".".join(file.split(".")[0:-1])
                module = importlib.import_module(r + "." + name_module)
                algorithms.append(module.__dict__[name_module])
    return algorithms

def create_order():
    ordered = []
    datasets = set()

    if subdir == 'data':
        datasets = get_data_reads

    elif subdir == 'merge_data':
        datasets = merge_data_reads

    # ----------------- Create an ordering of the algorithms based on the data sets that they read and write -----------------
    while len(algorithms) > 0:
        for i in range(0,len(algorithms)):
            if set(algorithms[i].reads).issubset(datasets):
                datasets = datasets | set(algorithms[i].writes)
                ordered.append(algorithms[i])
                del algorithms[i]
                break
    return ordered

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("contributor_folder")
    args = parser.parse_args()
    return args

if __name__ == "__main__":

    # ----------------- Parse command line args -----------------
    args = parse_args()
    subdir = args.contributor_folder

    # ----------------- Extract the algorithm classes the specified subdirectory -----------------
    algorithms = file_walk(subdir)

    # ----------------- Creates a correct ordering of get_data -> merge_data -----------------
    ordered = create_order()
    print()
    
    # ----------------- Execution -----------------
    for algorithm in ordered:
        algorithm.execute()