# quantum-incremental-SAT

This project consists of 2 parts, the SAT problem generator and the quantum solver.
To make use of both, we first need to have Python 3.7 or higher installed and the libraries it needs. These libraries can be obtained by executing the following command in the root of the project:
```console
$ pip install -r requirements.txt
```
Once we have installed everything we need, we use both utilities.

## Generador
The generator (generator.py) allows to generate k-SAT problems with different densities, number of variables, number of problems to generate, in addition to being able to put a seed on it. These examples are generated by default in the root within the \benchmark directory. The arguments it accepts are:

-v,--variables: A list with the number of variables in the SAT problems, required=True \
-k,--ksat: A list with the number of variables per clause in the SAT problems, required=True \
-d,--densities: A list with the densities in the SAT problems, required=True \
-e,--examples: The number of SAT problems per case, required=True \
-s,--seed: Seed for the random generator, required=False \
-p,--path: Path for the benchmark folder, required=False 

The set of problems that is generated in the repository has been generated with the following command executed in the root:

```console
$ python generator.py -v 5 6 7 8 9 10 11 12 13 14 15 16 --densities 2 3 4 5 -k 3 -e 10 --seed 1
```

To generate a new set of problems it is necessary to first delete the \benchmark directory.

## Solver
The solver is used to solve all the problems in the \ benchmark directory with the algorithm proposed in the article. It consists of a progress system that allows it to be stopped and executed, returning to the point where it was. The file where it is saving the results is called "results.pickle" and it creates it in the root. If you see that it is consuming a lot of RAM, you can stop with "Ctrl + C" and launch it again starting from the state in which it was left but with the RAM memory released. When the algorithm finishes solving all the problems, it generates a csv file (export_dataframe.csv) with the results data. This solver runs each problem 5 times with different seeds.

To run the solver you have to run the following command at the root of the project:

```console
$ python main.py
```
