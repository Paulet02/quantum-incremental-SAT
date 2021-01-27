import math


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