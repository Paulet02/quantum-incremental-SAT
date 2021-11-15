import qsimov as qj
import numpy as np
import copy
import networkx as nx
import math
from collections import OrderedDict
from code.util import utils
import sympy as sp
import os
import random
import sys
sys.path.insert(0,os.path.dirname(os.path.realpath(__file__)))



class Quantum_DSAT:#first most significant

    #random.seed(1)

    x_n = []
    x_i = []
    conf = {}
    sat_n = []
    sat = []
    nc = []
    nc_1 = []
    nc_2 = []
    sat_i = []
    s_1 = []
    s_2 = []

    total_iterations = 0
    max_n_variables_superposed = 0
    max_n_clauses_in_oracle = 0
    max_qubits_grover = 0

    heuristic_clauses = None

    best_conf = {}

    
    def __init__(self, dimacs_path=None, selection_heuristic=None, seed=0, quantum_simulation=False):
        random.seed(seed)
        self.heuristic_clauses = selection_heuristic
        self.quantum_simulation = quantum_simulation
        if(dimacs_path):
            current_path = os.path.dirname(os.path.abspath(__file__))
            self.n_variables, self.n_clauses, self.sat_n = utils.get_data_dimacs(dimacs_path)
    
    
    
    def solve(self):
        self.x_n = utils.variables(self.sat_n)
        if self.heuristic_clauses:
            clauses = [clause for clause in self.heuristic_clauses(self.sat_n)]
            for i in range(len(clauses)):
                self.sat.append(clauses[i]['clause'])
        else:
            self.sat = copy.deepcopy(self.sat_n)
        cont = 1
        self.sat_i = []
        while len(self.sat_i) < len(self.sat_n):
            clause = self.sat.pop(0)
            #clause2 = self.sat.pop(0)
            
            self.x_i = utils.variables(self.sat_i)
            self.nc = [clause]
            
            #print("-------------------------Iteración: "+str(cont)+"---------------------------------")
            #print("Última configuración ", self.conf)
            #print("Sat_i ", self.sat_i)
            #print("NC ", self.nc)

            #print("----------------------------------------------------------")
            

            if not self.step_1():
                return "SAT doesn't have solution", self.total_iterations, self.max_n_variables_superposed, self.max_n_clauses_in_oracle
            else:
                self.step_2()
                self.step_3()
                if self.step_4():
                    self.step_7()
                else:
                    if self.step_5():
                        if not self.step_7():
                            return "SAT doesn't have solution", self.total_iterations, self.max_n_variables_superposed, self.max_n_clauses_in_oracle
                    else:
                        if self.step_6():
                            if not self.step_7():
                                return "SAT doesn't have solution", self.total_iterations, self.max_n_variables_superposed, self.max_n_clauses_in_oracle
                        else:
                            return "SAT doesn't have solution", self.total_iterations, self.max_n_variables_superposed, self.max_n_clauses_in_oracle
            self.sat_i.append(clause)
            #self.sat_i.append(clause2)
            cont = cont + 1
        return self.conf, self.total_iterations, self.max_n_variables_superposed, self.max_n_clauses_in_oracle, self.max_qubits_grover
                        
    def step_1(self):
        #print("----> Step 1 <----")
        one_length_clauses = list(filter(lambda x: len(x) == 1, self.nc))
        literals = set()
        for [l] in one_length_clauses:
            if -l in literals:
                return False
            else:
                literals.add(l)
        return True
    def step_2(self):#not necessary
        #print("----> Step 2 <----")
        new_nc = []
        for clause in self.nc:
            literals = set()
            simplify = False
            for literal in clause:
                if -literal in literals:
                    simplify = True
                else:
                    literals.add(literal)
            if not simplify:
                new_nc.append(clause)
        self.nc = new_nc
        
    def step_3(self):
        #print("----> Step 3 <----")
        #print(self.sat_i)
        changed = True
        self.nc_1 = []
        self.nc_2 = []
        aux = copy.deepcopy(self.nc)
        while changed:
            changed = False
            for clause in aux:
                set1 = set(utils.variables(self.nc_1) + utils.variables(self.sat_i))
                set2 = set(utils.variables_in_clause(clause))
                if (len(set1.intersection(set2)) > 0):
                    self.nc_1.append(clause)
                    changed = True
                else:
                    self.nc_2.append(clause)
            aux = copy.deepcopy(self.nc_2)
            self.nc_2 = []
        self.nc_2 = copy.deepcopy(aux)

        changed = True
        self.s_1 = []
        self.s_2 = []
        aux = copy.deepcopy(self.sat_i)
        while changed:
            changed = False
            for clause in aux:
                set1 = set(utils.variables(self.nc) + utils.variables(self.s_1))
                set2 = set(utils.variables_in_clause(clause))
                if (len(set1 & set2) > 0):
                    self.s_1.append(clause)
                    changed = True
                else:
                    self.s_2.append(clause)
            aux = copy.deepcopy(self.s_2)
            self.s_2 = []
        self.s_2 = copy.deepcopy(aux)

       

    def step_4(self):
        #print("----> Step 4 <----")
        #print(self.nc_1, self.conf, self.nc_2)
        return utils.evaluate(self.nc_1, self.conf)
    
    def step_5(self):
        #print("----> Step 5 <----")
        set1 = set(utils.variables(self.nc_1))
        set2 = set(utils.variables(self.s_1))

        fixed = set1 & set2
        not_fixed = set1 - set2
        not_fixed_fixed = set()
        not_fixed_not_fixed = set()

        for var in not_fixed:
            if var not in self.best_conf.keys():
                not_fixed_not_fixed.add(var)
            else:
                not_fixed_fixed.add(var)

        #backtracking_sets_vars = utils.findsubsets(not_fixed, length)
        '''
        for var in not_fixed:
            if var in self.conf:
                not_fixed_fixed.add(var)
            else:
                not_fixed_not_fixed.add(var)

        #if there are no variable to superpose then go back in assignment
        if len(not_fixed_not_fixed) == 0:
            next_var = not_fixed_fixed.pop()
            if self.conf.pop(next_var, 3000) == 3000:
                print("algo pasa")
            if self.conf.pop(-next_var, 3000) == 3000:
                print("algo pasa 2")
            not_fixed_not_fixed.add(next_var)
        '''
        solution = False
        length = 1
        new_conf = copy.deepcopy(self.best_conf)

        if len(not_fixed_fixed) == 0:
            #print("Estoy en una sola iteracion porque no hay subsets")
            variables_oracle = utils.variables(self.nc_1)
            #{var: mode}
            variables = {}
            for var in variables_oracle:
                if var in new_conf.keys():
                    if new_conf[var]:
                        variables[var] = 1
                    else:
                        variables[var] = 0
                else:
                    variables[var] = 2
            solution = self.create_custom_Grover(variables, self.nc_1)
            #print("---------------------************--------------")
            #print(solution)
            #print("---------------------************--------------")
            if solution:
                self.conf.update(solution)
                self.best_conf.update(solution)
                return True
        else:

            while length <= len(not_fixed_fixed):

                backtracking_sets_vars = utils.findsubsets(not_fixed_fixed, length)
                for set_var in backtracking_sets_vars:
                    new_conf = copy.deepcopy(self.best_conf)
                    for variable in set_var:
                        if new_conf.pop(variable, 3000) == 3000:
                            print("algo pasa")
                        if new_conf.pop(-variable, 3000) == 3000:
                            print("algo pasa")
                    
                    variables_oracle = utils.variables(self.nc_1)
                    #{var: mode}
                    variables = {}
                    for var in variables_oracle:
                        if var in new_conf.keys():
                            if new_conf[var]:
                                variables[var] = 1
                            else:
                                variables[var] = 0
                        else:
                            variables[var] = 2
                    #call grover
                    solution = self.create_custom_Grover(variables, self.nc_1)
                    if solution:
                        self.conf.update(solution)
                        self.best_conf.update(solution)
                        return True
                length = length + 1
            
        return False
     
    def step_6(self):
        #print("----> Step 6 <----")
        
        count = 1
        elements = utils.variables_in_dict(self.best_conf)#sort by heuristic?
        n_fixed = len(elements)
        new_conf = {}
        solution = False
        length = 1

        while length <= n_fixed:
            backtracking_sets_vars = utils.findsubsets(elements, length)
            for set_var in backtracking_sets_vars:
                new_conf = copy.deepcopy(self.best_conf)
                for variable in set_var:
                    if new_conf.pop(variable, 3000) == 3000:
                        print("algo pasa")
                    if new_conf.pop(-variable, 3000) == 3000:
                        print("algo pasa")
                variables_oracle = utils.variables(self.nc_1 + self.s_1)
                #{var: mode}
                variables = {}
                for var in variables_oracle:
                    if var in new_conf.keys():
                        if new_conf[var]:
                            variables[var] = 1
                        else:
                            variables[var] = 0
                    else:
                        variables[var] = 2
                #call grover
                solution = self.create_custom_Grover(variables, self.nc_1 + self.s_1)
                if solution:
                    self.conf.update(solution)
                    self.best_conf.update(solution)
                    return True
            length = length + 1
        return False

    def step_7(self):
        #print("----> Step 7 <----")
        if len(self.nc_2) > 0:
            variables_oracle = utils.variables(self.nc_2)
            variables = {}
            for var in variables_oracle:
                variables[var] = 2
            solution = self.create_custom_Grover(variables, self.nc_2)
            #print("---------------------************--------------")
            #print(solution)
            #print("---------------------************--------------")
            if solution:
                self.conf = copy.deepcopy({**self.conf, **solution})
                self.best_conf = copy.deepcopy({**self.best_conf, **solution})
                return True
            else:
                return False
        return True
        
        
    def create_Grover_algorithm(self, input_qubits, ancilla_qubits=0, extra_qubit=True, input_variables_mode=None, oracle=None, uncomputation_oracle=None):
        grover_algorithm = qj.QCircuit(name="Grover's algorithm")
        iterations = int(round((np.pi*np.sqrt(2**input_qubits))/4))
        #print(iterations)
        #obtener dimention
        dim=10
        if extra_qubit:
            superposition = [qj.H(1) if i < input_qubits else qj.I(1) for i in range(0,dim - 1)]
            superposition.append(qj.PauliX())
            grover_algorithm.addLine(*superposition)
            #print(grover_algorithm.lines)
        else:
            superposition = [qj.H(1) if i < input_qubits else qj.I(1) for i in range(0, dim)]
            grover_algorithm.addLine(*superposition)
            #print(grover_algorithm.lines)
        grover_iteration = qj.QGate(name="Grover's iteration")
        grover_iteration.addLine(oracle)
        if uncomputation_oracle:
            grover_iteration.addLine(uncomputation_oracle)
        #ism=
        #grover_iteration.addLine(ism)
        for i in range(iterations):
            grover_algorithm.addLine(grover_iteration)
        #print(grover_algorithm.lines)
        
        
        #variables: a dict with all variables and their mode, 0 -> I; 1 -> X; 2 -> H
    def create_Grover(self, variables, clauses):
        #superposition = qj.QGate("Superposition")
        superposition = self.custom_Superposition(variables, mapping)#reverse?
        
        oracle = qj.QGate("Oracle")
        u_w=qj.QGate("Weights")
        pass
    
    #works, less significant to most [0,1,2,3,...,2^n-1]
    def custom_ISM_normal(self, variables_mode):#0 -> I; 1 -> X; 2 -> H
        #first most significant
        gates = {0:'I', 1:'X', 2:'H'}
        ism_custom  = qj.QGate("Inversion about the mean custom")
        #
        custom_superposition = self.custom_Superposition_normal(variables_mode)
        #print("custom_superposition")
        #print(custom_superposition.lines)
        #Line negation
        line_negation = qj.QGate("Line negation")
        line_negation.addLine(*['X' for i in range(len(variables_mode))])
        #Controlled-n Z
        controlled_Z = self.controlled_Z(len(variables_mode)-1)
        #construct the operator
        ism_custom.addLine(custom_superposition)
        ism_custom.addLine(line_negation)
        ism_custom.addLine(controlled_Z)
        ism_custom.addLine(line_negation)#qj.dagger(line_negation))
        ism_custom.addLine(custom_superposition)#qj.dagger(custom_superposition))
        #print("esta es custom superposition")
        #print(ism_custom.lines)
        return ism_custom
        
    #works, less significant to most [0,1,2,3,...,2^n-1]
    #mapping: key: value -> sat var -> qubit position
    def custom_ISM(self, variables_mode, mapping):#0 -> I; 1 -> X; 2 -> H
        #first most significant
        gates = {0:'I', 1:'X', 2:'H'}
        ism_custom  = qj.QGate("Inversion about the mean custom")
        #
        custom_superposition = self.custom_Superposition(variables_mode, mapping)
        #print("custom_superposition")
        #print(custom_superposition.lines)
        #Line negation
        line_negation = qj.QGate("Line negation")
        for var in mapping.keys():
            line_negation.addLine(*['X' if i == mapping[var] else None for i in range(len(mapping))])
            
        controls = list(mapping.values())
        #print("Esto son los controles", controls)
        #print(line_negation.lines)
        z_gate = controls.pop()
        controlled_Z = qj.QGate("Controlled Z")
        controlled_Z.addLine(*[['Z', controls, None] if i == z_gate else None for i in range(len(mapping))])
        #print(controlled_Z.lines)
        #construct the operator
        ism_custom.addLine(custom_superposition)
        ism_custom.addLine(line_negation)
        ism_custom.addLine(controlled_Z)
        ism_custom.addLine(line_negation)#qj.dagger(line_negation))
        ism_custom.addLine(custom_superposition)#qj.dagger(custom_superposition))
        #print("esta es custom superposition")
        #print(ism_custom.lines)
        return ism_custom
        ###########izquierda menos significativo
        #mapping: key: value -> sat var -> qubit position
    def custom_Superposition(self, variables_mode, mapping):#0 -> I; 1 -> X; 2 -> H
        cont = 0
        for value in variables_mode.values():
            if value == 2:
                cont = cont + 1
        #self.max_n_variables_superposed = max(cont, self.max_n_variables_superposed)


        #first most significant
        gates = {0:'I', 1:'X', 2:'H'}
        n_qubits = max(mapping.values())+1
        #literals_ordered = self.variables(clauses)
        #literals_ordered.sort()
        #print("la longitud es:",len(variables_mode), variables_mode)
        #print("la longitud es:",len(mapping), mapping)
        custom_superposition = qj.QGate("Custom superposition")
        for var in mapping.keys():
            custom_superposition.addLine(*[gates[variables_mode[var]] if i == mapping[var] else None for i in range(n_qubits)])
            #[gates[variables_mode[var]] if i == mapping[var] else None for i in range(len(variables_mode))]
        
        #print(custom_superposition.lines)
        #custom_superposition.addLine(*[gates[g] for g in variables_mode])
        return custom_superposition
    
    def custom_Superposition_normal(self, variables_mode):#0 -> I; 1 -> X; 2 -> H
        #first most significant
        gates = {0:'I', 1:'X', 2:'H'}
        custom_superposition = qj.QGate("Custom superposition")
        custom_superposition.addLine(*[gates[g] for g in variables_mode])
        return custom_superposition
        
    
    

    
    #most significant the results
    def construct_oracle_from_clauses(self, clauses):
        #update max number of clauses
        #self.max_n_clauses_in_oracle = max(len(clauses), self.max_n_clauses_in_oracle)

        #order the literals 1 less significant
        literals_ordered = utils.variables(clauses)
        literals_ordered.sort()
        
        #generate the map between variables and qubits
        mapping = {}
        for var in literals_ordered:
            mapping[var] = len(mapping)
        #print(mapping)
        
        #calculate the necessary extra qubits
        n_extra_qubits = len(clauses)
        
        #to conjunction of conjunctions (De Morgan)
        new_clauses = list(map(lambda x: list(map(lambda y: y * (-1), x)), clauses)) # each clause goes negate
        #print(clauses)
        #print(new_clauses)
        
        cont = 0
        oracle_gates = []
        unoracle_gates = []
        for clause in new_clauses:
            gate = qj.QGate("Clause "+str(cont))
            ungate = qj.QGate("UnClause "+str(cont))
            controls, anticontrols = utils.split_literals(clause)
            controls = list(map(lambda x: mapping[abs(x)], controls))
            anticontrols = list(map(lambda x: mapping[abs(x)], anticontrols))
            #print("controles y anticontroles")
            #print(controls,anticontrols)
            #compute the clause
            gate.addLine(*[None for i in range(len(literals_ordered) + cont)], ['X', controls, anticontrols], *[None for i in range(n_extra_qubits - cont)])
            #print(gate.lines)
            #negates the entire clause
            gate.addLine(*[None for i in range(len(literals_ordered) + cont)], ['X', [], []], *[None for i in range(n_extra_qubits - cont)])
            #print(gate.lines)
            ungate.addLine(*[None for i in range(len(literals_ordered) + cont)], ['X', [], []], *[None for i in range(n_extra_qubits - cont)])
            ungate.addLine(*[None for i in range(len(literals_ordered) + cont)], ['X', controls, anticontrols], *[None for i in range(n_extra_qubits - cont)])
            
            #add the gates to the array
            oracle_gates.append(copy.deepcopy(gate))
            unoracle_gates.insert(0, copy.deepcopy(ungate))
            #print("Estas son las gates")
            #print(gate.lines)
            
            #increase auxiliar qubit
            cont = cont + 1
            
        gate = qj.QGate("Total conjunction")
        #gate.addLine(*[None for i in range(len(literals_ordered) + n_extra_qubits)], ['Z', [i for i in range(len(literals_ordered), len(literals_ordered) + n_extra_qubits)], []])
        gate.addLine(*[None for i in range(len(literals_ordered) + n_extra_qubits)], ['X', [i for i in range(len(literals_ordered), len(literals_ordered) + n_extra_qubits)], []])
        #print("++++++++++++++++++++")
        #print(gate.lines)
        oracle_gates.append(gate)
        unoracle_gates.insert(0, copy.deepcopy(gate))
        #create the oracle
        oracle = qj.QGate("Oracle")
        for gate in oracle_gates:
            oracle.addLine(gate)
        #create the unoracle
        unoracle = qj.QGate("Unoracle")
        for gate in unoracle_gates:
            unoracle.addLine(gate)
        #print(oracle_gates)
        #print(unoracle_gates)
        #print(oracle.lines)
        #print(unoracle.lines)
        return oracle, unoracle, mapping
            
    def controlled_Z(self, n_control):#works, the Z in the most significant (last position)
        controlled_Z  = qj.QGate("Controlled^n Z")
        line = []
        for i in range(n_control):
            line.append(None)
        z_controls = [i - 1 for i in range(1, n_control + 1)]
        line.append(['Z', z_controls])
        controlled_Z.addLine(*line)
        
        #CnZ=qj.PauliZ()
        #for i in range(n_control):
        #    CnZ=qj.CU(CnZ)
        #controlled_Z.addLine(CnZ)
        #print(controlled_Z.lines)
        return controlled_Z
    
    def oracle(self, sol):
        gates = {1:qj.I(1), 0:qj.PauliX()}
        negation = qj.QGate("Negation solution")
        negation.addLine(*[gates[g] for g in sol])
        oracle = qj.QGate("Oracle")
        oracle.addLine(negation, qj.I(1))
        oracle.addLine(self.controlled_Z(len(sol)))
        oracle.addLine(negation, qj.I(1))
        return oracle
    
    def test(self):
        N=1
        mp_n = qj.QCircuit(name="McCulloch-Pitts neuron")
        input_operator = qj.QGate("Input pattern")
        input_operator.addLine(qj.H(N),qj.I(1))
        mp_n.addLine(input_operator)
        print ("Created!")
        #print (mp_n.lines[0][0].lines)
        #print ("Executing McCulloch-Pitts neuron circuit...")
        reg=mp_n.execute(N+1)
        #print ("Done!")

    
    #variables dict var: mode
    #0 -> I; 1 -> X; 2 -> H
    def create_custom_Grover(self, variables, clauses):
        unknown_variables = 0
        configuration = {}
        for variable in variables.keys():
            if variables[variable] == 0:
                configuration[variable] = False
                configuration[-variable] = True
            if variables[variable] == 1:
                configuration[-variable] = False
                configuration[variable] = True
            if variables[variable] == 2:
                unknown_variables = unknown_variables + 1

        k_solutions = utils.get_number_solutions(clauses, conf=configuration)
        n_iterations = utils.iterations(unknown_variables, k_solutions)
        
        n_iterations_rounded = int(round(n_iterations))
        #mapping var -> position
        oracle, unoracle, mapping = self.construct_oracle_from_clauses(clauses)
        custom_superposition = self.custom_Superposition(variables, mapping)

        custom_ISM = self.custom_ISM(variables, mapping)
        n_qubits = len(variables) + len(clauses) + 1
        grover_algorithm = qj.QGate("Grover's algorithm")
        grover_algorithm.addLine(*[None for i in range(n_qubits)])
        quantum = False
        if n_iterations_rounded >= 1:
            self.total_iterations = self.total_iterations + n_iterations_rounded
            self.max_n_variables_superposed = max(self.max_n_variables_superposed, unknown_variables)
            self.max_n_clauses_in_oracle = max(self.max_n_clauses_in_oracle, len(clauses))
            self.max_qubits_grover = max(self.max_qubits_grover, n_qubits)
            grover_algorithm.addLine(custom_superposition, *[None for i in range(len(clauses) + 1)])
            for i in range(n_iterations_rounded):
                grover_algorithm.addLine(oracle)
                grover_algorithm.addLine(*['Z' if i == (len(variables) + len(clauses)) else None for i in range(len(variables) + len(clauses) + 1)])
                grover_algorithm.addLine(unoracle)
                grover_algorithm.addLine(custom_ISM, *[None for i in range(len(clauses) + 1)])
            quantum = True
        elif n_iterations_rounded < 1 and n_iterations_rounded >= 0:
            solution = utils.get_solution(clauses, conf=configuration)
            #print("El numero de iteraciones con demasiadas iteraciones es: ", n_iterations_rounded)
            self.total_iterations = self.total_iterations + 1#0
            #print(solution)
            #print("demasiadas soluciones")
            quantum = False
            pass#do partial grover technique
        else:
            solution = {}

        if quantum:
            if self.quantum_simulation:
                reg = qj.QRegistry(len(variables) + len(clauses) + 1)
                reg.applyGate(grover_algorithm)
                print(reg.getState())
                result = utils.get_max_state(reg.getState())
                bin_number = list(format(result, '0' + str(n_qubits) + 'b'))
                print(bin_number)
                bin_number.reverse()
                solution = {}
                for var in mapping:
                    if bin_number[mapping[var]] == '0':
                        solution[var] = False
                        solution[-var] = True
                    elif bin_number[mapping[var]] == '1':
                        solution[var] = True
                        solution[-var] = False
                print(bin_number)
            else:
                solution = utils.get_solution(clauses, conf=configuration)
            
        if utils.evaluate(clauses, solution):
            return solution
        else:
            return {}

    
    
    
    def create_arbitrary_superposition(self, mask):#cambiar n por N
        custom_amplitudes = qj.QGate("Arbitrary superposition")
        #custom_amplitudes.addLine(*[gates[g] for g in variables_mode])
        N=int(sp.log(len(mask),2).evalf())
        n=2**N
        #mask.reverse()
        angles={}
        for i in range(N):
            for j in range(2**i):
                controls = []
                anticontrols = []
                bin_number=[0 if (len("{0:b}".format(j))+k)-(i)<0 else int("{0:b}".format(j)[len("{0:b}".format(j))+k-(i)]) for k in range(i)]
                bin_number.reverse()
                #if i==0:
                #   alpha='alpha'+str(i+1)
                #else:
                prefix=''.join(str(element) for element in bin_number)
                controls = []
                anticontrols = []
                print(bin_number)
                
                for k in range(len(bin_number)):
                    if bin_number[k]:
                        print("control")
                        controls.append(k)
                    else:
                        print("anticontrol")
                        anticontrols.append(k)
                alpha='alpha'+str(i+1)+'_'+''.join(str(element) for element in bin_number)
                
                qubit_rotation = i
                
                #angles[alpha]=i
                
                
                numerator=0
                denominator=0
                for k in range(2**(N-(i+1))):
                    bin_number=[0 if (len("{0:b}".format(k))+l)-(N-(i+1))<0 else int("{0:b}".format(k)[len("{0:b}".format(k))+l-(N-(i+1))]) for l in range(N-(i+1))]
                    aux_prefix_numerator=prefix+'1'+''.join(str(element) for element in bin_number)
                    aux_prefix_denominator=prefix+'0'+''.join(str(element) for element in bin_number)
                    
                    print(int(aux_prefix_numerator, 2))
                    print(int(aux_prefix_denominator, 2))
                    numerator=numerator+mask[int(aux_prefix_numerator, 2)]**2
                    denominator=denominator+mask[int(aux_prefix_denominator, 2)]**2
                
                
                
                if numerator!=0 and denominator!=0:
                    angles[alpha]=sp.rad(sp.deg(sp.atan(sp.sqrt(numerator/denominator)))).evalf()
                else:
                    angles[alpha]=None
                print(qubit_rotation, angles[alpha], controls, anticontrols)
                angle = angles[alpha]
                #in radians
                custom_amplitudes.addLine(*[['U('+str(angle*2)+',0,pi)',controls,anticontrols] if i == qubit_rotation else None for i in range(N)])
        #print(angles)
        #print(custom_amplitudes.lines)
        reg = qj.QRegistry(N)
        reg.applyGate(custom_amplitudes)
        utils.print_amplitudes(reg.getState())
        #print(reg.getState())
        return custom_amplitudes

    