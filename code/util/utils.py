import math
import copy
import numpy as np
import cmath
import itertools
import random
import os
from code.solver.quantum_solver import Quantum_DSAT

def variables(clauses):
        return literals(list(map(lambda x: list(map(lambda y: abs(y), x)), clauses)))
    
def literals(clauses):
    literals = set()
    for clause in clauses:
        for literal in clause:
            literals.add(literal)
    return list(literals)

def iterations(n_variables, k_solutions):
    if k_solutions == 0:
        return -1
    return (math.pi / 4) * (2**n_variables / k_solutions)**(1/2) - 0.5

#mapping key:val -> bin position -> variable
def bin_generator(n):
    for i in range(2**n):
        bin_number = list(format(i, '0' + str(n) + 'b'))
        bin_number.reverse()
        yield bin_number

def evaluate(sat, conf):
    evaluation = []
    for clause in sat:
        evaluation.append(any(list(map(lambda x: conf.get(x), clause))))
    return all(evaluation)

def variables_in_clause(clause):
    return list(set([abs(var) for var in clause]))

def distance(c1, c2):
    vars1 = variables_in_clause(c1)
    vars2 = variables_in_clause(c2)
    variables = set(vars1 + vars2)
    return len(c1) + len(c2) - len(variables)

def split_literals(clause):
    normal = list(filter(lambda x: x > 0, clause))
    negate = list(filter(lambda x: x < 0, clause))
    return normal, negate

            
def appearances_in(clauses_a, clauses_b):
    appears = []
    not_appears = []
    variables_a = variables(clauses_a)
    variables_b = variables(clauses_b)
    for variable in variables_a:
        if variable in variables_b:
            appears.append(variable)
        else:
            not_appears.append(variable)
    return appears, not_appears

#take into account the fixed variables
def get_number_solutions(sat, conf={}):
    variables_list = variables(sat)
    variables_list.sort()
    
    fixed_variables = list(conf.keys())
    
    #generate the map between variables and qubits and variables and bin number
    mapping_bin = {}
    mapping = {}
    for var in variables_list:
        mapping[len(mapping)] = var
        if var not in conf.keys():
            mapping_bin[len(mapping_bin)] = var
            
    n = len(variables(sat))
    n_unknown_variables = n-int(len(fixed_variables)/2)
    
    solutions = 0
    
    binary_generator = bin_generator(n_unknown_variables)
    for bin_number in binary_generator:
        configuration = {}
        configuration = copy.deepcopy(conf)
        
        for j in range(len(bin_number)):
            if j in mapping_bin.keys():
                if bin_number[j] == '0':
                    configuration[mapping_bin[j]] = False
                    configuration[-mapping_bin[j]] = True
                else:
                    configuration[mapping_bin[j]] = True
                    configuration[-mapping_bin[j]] = False
        if evaluate(sat, configuration):
            solutions = solutions + 1
            bin_number.reverse()
    return solutions

#https://toughsat.appspot.com/
def get_data_dimacs(path):
    file = open(path, 'r') 
    lines = file.readlines() 
    n_variables = 0
    n_clauses = 0
    count = 0
    clauses = []
    for line in lines:
        if count == 1:
            n_variables = int(line.split()[2])
            n_clauses = int(line.split()[3])
        elif count > 1:
            ls = list(map(int, line.split()[:-1]))
            clauses.append(ls)
        count = count + 1
    return n_variables, n_clauses, clauses

def print_amplitudes(state):
    n_qubits=int(np.log2(len(state)))
    for j in range(len(state)):
        bin_number=[0 if (len("{0:b}".format(j))+i)-(n_qubits)<0 else int("{0:b}".format(j)[len("{0:b}".format(j))+i-(n_qubits)]) for i in range(n_qubits)]
        print(str(j)+"   "+str(bin_number)+"     "+str(state[j]))

def get_max_state(state):
    aux = 0
    n = 0
    for j in range(len(state)):
        
        if cmath.polar(state[j])[0] > aux:
            aux = copy.deepcopy(cmath.polar(state[j])[0])
            n = j
    return n

def get_solution(sat, conf={}):
    variables_list = variables(sat)
    variables_list.sort()
    
    fixed_variables = list(conf.keys())
    configurations = []
    #generate the map between variables and qubits and variables and bin number
    mapping_bin = {}
    mapping = {}
    for var in variables_list:
        mapping[len(mapping)] = var
        if var not in conf.keys():
            mapping_bin[len(mapping_bin)] = var
            
    n = len(variables(sat))
    n_unknown_variables = n-int(len(fixed_variables)/2)

    solutions = 0
    
    binary_generator = bin_generator(n_unknown_variables)
    for bin_number in binary_generator:
        
        configuration = {}
        configuration = copy.deepcopy(conf)
        
        for j in range(len(bin_number)):
            if bin_number[j] == '0':
                configuration[mapping_bin[j]] = False
                configuration[-mapping_bin[j]] = True
            else:
                configuration[mapping_bin[j]] = True
                configuration[-mapping_bin[j]] = False
        if evaluate(sat, configuration):
            solutions = solutions + 1
            bin_number.reverse()
            configurations.append(configuration)
    if len(configurations) == 0:
        return {}
    else:
        return random.choice(configurations)

def findsubsets(s, n):
    return itertools.combinations(s, n)

def variables_in_dict(dict):
    vars = set()
    for key in dict.keys():
        vars.add(abs(key))
    return vars

def heuristic_sort_by_appearances(clauses):
    variables_clauses = variables(clauses)
    variables_all_appearances = list(itertools.chain(*clauses))

    clauses_sorted = []
    variables_info = []
    variables_min = {}
    for variable in variables_clauses:
        i_a = variables_all_appearances.count(variable)
        i_n = variables_all_appearances.count(-variable)
        variables_info.append({'variable': variable, 'i_a': i_a, 'i_n': i_n, 'i_min': min(i_a, i_n)})
        variables_min[variable] = min(i_a, i_n)
    variables_info.sort(key=lambda x: x['i_min'], reverse=True)

    first = variables_info[0]['i_min']
    second = variables_info[1]['i_min']
    third = variables_info[2]['i_min']

    distance = lambda i, j, k, st, nd, rd: 1/3**i + 1/3**j + 1/3**k - 1/3**st - 1/3**nd - 1/3**rd

    for clause in clauses:
        clauses_sorted.append({'clause': clause, 'distance': round(distance(variables_min[abs(clause[0])], variables_min[abs(clause[1])], variables_min[abs(clause[2])], first, second, third), 5)})

    clauses_sorted.sort(key=lambda x: x['distance'])
    return clauses_sorted

def is_satisfiable(sat, conf={}):
    variables_list = variables(sat)
    variables_list.sort()
    
    fixed_variables = list(conf.keys())
    
    #generate the map between variables and qubits and variables and bin number
    mapping_bin = {}
    mapping = {}
    for var in variables_list:
        mapping[len(mapping)] = var
        if var not in conf.keys():
            mapping_bin[len(mapping_bin)] = var
            
    n = len(variables(sat))
    n_unknown_variables = n-int(len(fixed_variables)/2)

    binary_generator = bin_generator(n_unknown_variables)
    for bin_number in binary_generator:
        configuration = {}
        configuration = copy.deepcopy(conf)
        for j in range(len(bin_number)):
            if j in mapping_bin.keys():
                if bin_number[j] == '0':
                    configuration[mapping_bin[j]] = False
                    configuration[-mapping_bin[j]] = True
                else:
                    configuration[mapping_bin[j]] = True
                    configuration[-mapping_bin[j]] = False
        if evaluate(sat, configuration):
            return True
    return False


def get_results(file, seed, q_simulation):
    n_variables, n_clauses, clauses = get_data_dimacs(file)
    filename = os.path.splitext(os.path.basename(file))[0]
    print(filename)
    
    solutions = get_number_solutions(clauses)
    nosol=0
    if solutions:
        #############without heuristic
        q_sat = Quantum_DSAT(file, seed=seed, quantum_simulation=q_simulation)
        conf, total_iterations, max_n_variables_superposed, max_n_clauses_in_oracle, max_qubits_grover = q_sat.solve()
        row_natural = {'Algorithm': 'Incremental Grover-based',
            'Number of variables': n_variables,
            'Number of clauses': n_clauses,
            'Max number of variables superposed': max_n_variables_superposed,
            'Max number of clauses in oracle': max_n_clauses_in_oracle, 
            'Total iterations': total_iterations,
            'Max number of qubits used in circuit': max_qubits_grover,
            'Heuristic': "Natural order",
            'Seed': seed,
            'Example': filename,
            'Solution': conf,
            'id': "Natural order_"+str(seed)+"_"+str(filename)}
        if evaluate(clauses, conf):
            #append row to the dataframe
            pass
        else:
            raise "Failed solution"
        ##############################

        ##############with heuristic
        q_sat = Quantum_DSAT(file, selection_heuristic=heuristic_sort_by_appearances, seed=seed, quantum_simulation=q_simulation)
        conf, total_iterations, max_n_variables_superposed, max_n_clauses_in_oracle, max_qubits_grover = q_sat.solve()
        
        row_heuristic = {'Algorithm': 'Incremental Grover-based',
            'Number of variables': n_variables,
            'Number of clauses': n_clauses,
            'Max number of variables superposed': max_n_variables_superposed,
            'Max number of clauses in oracle': max_n_clauses_in_oracle, 
            'Total iterations': total_iterations,
            'Max number of qubits used in circuit': max_qubits_grover,
            'Heuristic': "Heuristic's order",
            'Seed': seed,
            'Example': filename,
            'Solution': conf,
            'id': "Heuristic's order_"+str(seed)+"_"+str(filename)}
        if evaluate(clauses, conf):
            #append row to the dataframe
            pass
        else:
            raise "Failed solution"
        #############################

        row_grover = {'Algorithm': 'Grover original',
            'Number of variables': n_variables,
            'Number of clauses': n_clauses,
            'Max number of variables superposed': n_variables,
            'Max number of clauses in oracle': n_clauses, 
            'Total iterations': int(round(iterations(n_variables, solutions))),
            'Max number of qubits used in circuit': n_variables + n_clauses + 1,
            'Heuristic': 'Grover',
            'Seed': seed,
            'Example': filename,
            'Solution': conf,
            'id': "Grover_"+str(seed)+"_"+str(filename)}
        #append row to the dataframe
        
    else:
        nosol = nosol + 1

    return row_natural, row_heuristic, row_grover