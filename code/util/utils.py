import math
import copy


def variables(clauses):
        return literals(list(map(lambda x: list(map(lambda y: abs(y), x)), clauses)))
    
def literals(clauses):
    literals = set()
    for clause in clauses:
        for literal in clause:
            literals.add(literal)
    return list(literals)

def iterations(n_variables, k_solutions):
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
    return [abs(var) for var in clause]

def distance(c1, c2):#to test
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
def get_number_solutions(sat, conf={}):#to test, works fine
    variables_list = variables(sat)
    variables_list.sort()
    print("Las variables ordenadas: ",variables_list)
    fixed_variables = list(conf.keys())
    
    #generate the map between variables and qubits and variables and bin number
    mapping_bin = {}
    mapping = {}
    for var in variables_list:
        mapping[len(mapping)] = var
        if var not in conf.keys():
            mapping_bin[len(mapping_bin)] = var
    #mapping = OrderedDict(sorted(mapping.items(), key=lambda t: t[0]))
    print("los mappings")
    print(mapping)
    print(mapping_bin)
    n = len(variables(sat))
    n_unknown_variables = n-int(len(fixed_variables)/2)
    print(n)
    solutions = 0
    print(2**(n_unknown_variables))
    print(int(len(fixed_variables)/2))
    print(fixed_variables)
    binary_generator = bin_generator(n_unknown_variables)
    for bin_number in binary_generator:
        #bin_number = list(format(i, '0' + str(n_unknown_variables) + 'b'))
        #bin_number.reverse()
        configuration = {}
        configuration = copy.deepcopy(conf)
        print(configuration)
        print(bin_number)
        for j in range(len(bin_number)):
            #print(mapping[j],conf.keys(),conf,fixed_variables)
            if bin_number[j] == '0':
                configuration[mapping_bin[j]] = False
                configuration[-mapping_bin[j]] = True
            #       print("Estoy en el 0",j, configuration)
            else:
                configuration[mapping_bin[j]] = True
                configuration[-mapping_bin[j]] = False
            #      print("Estoy en el 1",j, configuration)
        print(configuration)
        if evaluate(sat, configuration):
            solutions = solutions + 1
            bin_number.reverse()
            print("Hay solucion en: " + str(bin_number))
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