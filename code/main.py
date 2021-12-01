import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from code.util.utils import *
from code.solver.quantum_solver import Quantum_DSAT
from pathlib import Path

import glob
import pandas as pd
import pickle
import json

import sys
sys.path.insert(0,os.path.dirname(os.path.realpath(__file__)))


path = os.path.dirname(os.path.realpath(__file__))
print("Current directory", path)
path_examples = os.path.dirname(os.path.realpath(__file__)) + '/solver/benchmark'
print(path_examples)
files = glob.glob(path_examples + '/**/*.dimacs', recursive=True)





seeds = [0, 1, 2, 3, 4]
pd.set_option('display.max_columns', None)
cont = 0
nosol=0
sol=0
print("Total files: ", len(files))
q_simulation = False

file_results = 'results.pickle'
if os.path.isfile(file_results):
    with open(file_results, 'rb') as f:
        data = pickle.load(f)
else:
    data = []

print("Load data: ", data)

ids = set()
for item in data:
    ids.add(item["id"])
print("Data ids: ",ids)

for seed in seeds:
    for file in files:
        print("Example ", cont, " of ", len(files)*len(seeds))
        filename = os.path.splitext(os.path.basename(file))[0]
        id_random = "Random order_"+str(seed)+"_"+str(filename)
        id_heuristic = "Heuristic's order_"+str(seed)+"_"+str(filename)
        id_grover = "Grover_"+str(seed)+"_"+str(filename)
        if id_random not in ids or id_heuristic not in ids or id_grover not in ids:
            row_natural, row_heuristic, row_grover = get_results(file, seed, q_simulation)
            if id_random not in ids:
                data.append(row_natural)
                ids.add(id_random)
            
            if id_heuristic not in ids:
                data.append(row_heuristic)
                ids.add(id_heuristic)
            
            if id_grover not in ids:
                data.append(row_grover)
                ids.add(id_grover)
            
        else:
            print("Already calculated")
        with open(file_results, 'wb') as f:
            pickle.dump(data, f)
        cont = cont + 1

df = pd.DataFrame.from_dict(data)

df.to_csv('export_dataframe.csv', index = False)



