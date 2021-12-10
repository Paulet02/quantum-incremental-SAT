import os
import sys
from code.util.utils import get_results
from pathlib import Path

import glob
import pandas as pd
import pickle
import json
import sys
from multiprocessing import Process, BoundedSemaphore
import os


#sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))


PATH = os.path.dirname(os.path.realpath(__file__))
PATH_EXAMPLES = os.path.dirname(os.path.realpath(__file__)) + '/benchmark'
RESULT_EXAMPLES = os.path.dirname(os.path.realpath(__file__)) + '/results'
SEEDS = [0, 1, 2, 3, 4]

def solve_file(f, seed, q_simulation, control):
    control.acquire()
    try:
        filename = os.path.splitext(os.path.basename(f))[0]
        print(f"Solving {filename}")
        results = get_results(f, seed, q_simulation)
        with open(f'{RESULT_EXAMPLES}/{filename}_{seed}.json', 'w') as fout:
            json.dump(results, fout)
        print(f'file generated {RESULT_EXAMPLES}/{filename}_{seed}.json')
    finally:
        control.release()

def main(maxproc):
    files = glob.glob(PATH_EXAMPLES + '/**/*.dimacs', recursive=True)
    q_simulation = False
    tasks = []
    control = BoundedSemaphore(maxproc)
    for seed in SEEDS:
        for f in files:
            print('.', end='')
            tasks.append(Process(target=solve_file,
                                 args=(f, seed, q_simulation, control)))

    print('starting')
    for p in tasks:
        p.start()
    for p in tasks:
        p.join()




if __name__ == '__main__':
    maxproc = int(sys.argv[1])
    main(maxproc)
