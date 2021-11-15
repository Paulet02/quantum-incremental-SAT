import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import unittest
from code.solver.quantum_solver import Quantum_DSAT



class QuantumSolverTest(unittest.TestCase):
	current_path = os.path.dirname(os.path.abspath(__file__))
	
	'''def test_step_1(self):
		nc1 = [[4,1],[-3],[2,-4],[5,3],[6,5,10],[11,-12],[11,13,-10],[3],[14,-16]]
		nc2 = [[4,1],[-3,-1],[4],[2,-4],[5,3],[6,5,10],[3],[11,-12],[11,13,-10],[14,15],[4],[14,-16]]
		
		q_sat = Quantum_DSAT()
		
		q_sat.nc = nc1
		result1 = q_sat.step_1()

		self.assertFalse(result1)

		q_sat.nc = nc2
		result2 = q_sat.step_1()

		self.assertTrue(result2)

	def test_step_2(self):
		nc1 = [[4,1],[-3],[2,-4],[5,3],[6,5,10],[11,-12],[11,13,-10],[3],[14,-16]]
		nc2 = [[4,1],[-3,-1],[4],[2,-4],[5,3],[6,5,10,-6],[3,3],[11,-12],[11,13,-10,-13],[14,15],[4,-4],[14,-16]]
		
		nc1_expected = [[4,1],[-3],[2,-4],[5,3],[6,5,10],[11,-12],[11,13,-10],[3],[14,-16]]
		nc2_expected = [[4,1],[-3,-1],[4],[2,-4],[5,3],[3,3],[11,-12],[14,15],[14,-16]]

		q_sat = Quantum_DSAT()
		
		q_sat.nc = nc1
		q_sat.step_2()
		q_sat.nc

		self.assertEqual(len(nc1_expected), len(q_sat.nc))
		for i in range(len(nc1_expected)):
			self.assertListEqual(nc1_expected[i], q_sat.nc[i])

		q_sat.nc = nc2
		q_sat.step_2()
		q_sat.nc

		self.assertEqual(len(nc2_expected), len(q_sat.nc))
		for i in range(len(nc2_expected)):
			self.assertListEqual(nc2_expected[i], q_sat.nc[i])

	def test_step_3(self):
		nc = [[4,1],[-3,-1],[2,-4],[5,3],[6,5,10],[11,-12],[11,13,-10],[14,15],[14,-16]]
		
		sat = [[-4,3,-2],[-3,-1],[4,3],[17,18],[19,20],[18,5]]

		nc_1_expected = [[4,1],[-3,-1],[2,-4],[5,3],[6,5,10],[11,13,-10],[11,-12]]
		nc_2_expected = [[14,15],[14,-16]]

		s_1_expected = [[-4,3,-2],[-3,-1],[4,3],[18,5],[17,18]]
		s_2_expected = [[19,20]]

		q_sat = Quantum_DSAT()
		
		q_sat.nc = nc
		q_sat.sat_i = sat
		q_sat.step_3()

		self.assertEqual(len(nc_1_expected), len(q_sat.nc_1))
		for i in range(len(nc_1_expected)):
			self.assertListEqual(nc_1_expected[i], q_sat.nc_1[i])

		self.assertEqual(len(nc_2_expected), len(q_sat.nc_2))
		for i in range(len(nc_2_expected)):
			self.assertListEqual(nc_2_expected[i], q_sat.nc_2[i])

		self.assertEqual(len(s_1_expected), len(q_sat.s_1))
		for i in range(len(s_1_expected)):
			self.assertListEqual(s_1_expected[i], q_sat.s_1[i])
		
		self.assertEqual(len(s_2_expected), len(q_sat.s_2))
		for i in range(len(s_2_expected)):
			self.assertListEqual(s_2_expected[i], q_sat.s_2[i])

	def test_step_4(self):#utils.evaluate(self.nc_1, self.conf)
		nc1_1 = [[4,1],[-4,3,2],[-3,-1],[2,-4],[4,3]]
		
		solution_expected_1 = {1: False, -1: True, 2: True, -2: False, 4: True, -4: False}
		
		solution_expected_2 = {1: False, -1: True, 2: True, -2: False, 3: True, -3: False, 4: False, -4: True}
		
		q_sat = Quantum_DSAT()
		
		q_sat.nc_1 = nc1_1
		q_sat.conf = solution_expected_1
		result1 = q_sat.step_4()

		self.assertTrue(result1)

		q_sat.nc_1 = nc1_1
		q_sat.conf = solution_expected_2
		result2 = q_sat.step_4()

		self.assertFalse(result2)

	def test_step_5(self):#utils.evaluate(self.nc_1, self.conf)
		nc1_1 = [[4,1],[-3,-1],[4,3],[-4,3,2]]
		s1_1 = [[2,-4]]
		conf_1 = {2: False, -2: True, 4: True, -4: False}
		
		solution_expected_1 = False

		nc1_2 = [[4,1],[-3,-1],[4,3],[-4,3,2]]
		s1_2 = [[2,-4]]
		conf_2 = {2: False, -2: True, 4: False, -4: True, 3: False, -3: True, 1: False, -1: True}
		
		solution_expected_2 = {1: True, -1: False, 2: True, -2: False, 3: True, -3: False, 4: False, -4: True}

		print("-----------------STEP 5----------------------")

		q_sat = Quantum_DSAT()
		
		q_sat.nc_1 = nc1_1
		q_sat.best_conf = conf_1
		q_sat.s_1 = s1_1
		result1 = q_sat.step_5()

		print("Esta es la solución: ", q_sat.best_conf)
		#self.assertFalse(result1)

		print("--------------------------Empieza la segunda")
		q_sat.nc_1 = nc1_2
		q_sat.best_conf = conf_2
		q_sat.s_1 = s1_2
		result2 = q_sat.step_5()

		print("Esta es la solución: ", q_sat.best_conf)
		#self.assertTrue(result2)
		#self.assertDictEqual(q_sat.conf, solution_expected_2)

	def test_step_6(self):#utils.evaluate(self.nc_1, self.conf)
		nc1_1 = [[4,1],[-3,-1],[4,3]]
		s1_1 = [[2,-4],[-4,3,2]]
		conf_1 = {2: False, -2: True, 4: False, -4: True}
		
		solution_expected_1 = {1: False, -1: True, 2: True, -2: False, 3: False, -3: True, 4: True, -4: False}
		expected_iterations = 3

		nc1_2 = [[4,1],[-3,-1],[4,3]]
		s1_2 = [[2,-4],[-4,3,2]]
		conf_2 = {2: False, -2: True, 4: False, -4: True, 3: False, -3: True, 1: False, -1: True}
		
		solution_expected_2 = {1: False, -1: True, 2: True, -2: False, 3: False, -3: True, 4: True, -4: False}
		expected_iterations_2 = 12

		print("-----------------STEP 6----------------------")

		q_sat = Quantum_DSAT()
		
		q_sat.nc_1 = nc1_1
		q_sat.best_conf = conf_1
		q_sat.s_1 = s1_1
		result1 = q_sat.step_6()

		self.assertTrue(result1)
		self.assertDictEqual(solution_expected_1, q_sat.conf)
		self.assertEqual(expected_iterations, q_sat.total_iterations)

		#print("Esta es la solución: ", q_sat.conf)
		#self.assertFalse(result1)

		print("--------------------------Empieza la segunda")
		q_sat.nc_1 = nc1_2
		q_sat.best_conf = conf_2
		q_sat.s_1 = s1_2

		result2 = q_sat.step_6()
		
		self.assertTrue(result2)
		self.assertDictEqual(solution_expected_2, q_sat.conf)
		self.assertEqual(expected_iterations_2, q_sat.total_iterations)

		#print("Esta es la solución: ", q_sat.conf)
		#self.assertTrue(result2)
		#self.assertDictEqual(q_sat.conf, solution_expected_2)

	def test_create_custom_Grover(self):
		q_sat = Quantum_DSAT()
		solution = q_sat.create_custom_Grover({1: 2,2: 2,3:2,4:2}, [[4,1],[-4,3,-2],[-3,-1],[2,-4],[4,3]])
		print("El sertuado ", solution)
		solution_expected = {1: False, -1: True, 2: True, -2: False, 3: True, -3: False, 4: True, -4: False}
		self.assertDictEqual(solution_expected, solution)'''

	def test_solve(self):
		print("Esto es sooooooolve")
		path = "3-sat-1.dimacs"
		q_sat = Quantum_DSAT(path)
		solution, iterations, n_variables, n_clauses = q_sat.solve()
		print("He acabado")
		print("La solución: ", solution)
		print("El número de iteraciones: ", iterations)
		print("El número de variables superpuestas máximas: ", n_variables)
		print("El número de cláusulas máximas ", n_clauses)
		print("El número de qubits máximos ", q_sat.max_qubits_grover)
		'''
		print("Esto es sooooooolve")
		path = "3-sat-4.dimacs"
		q_sat1 = Quantum_DSAT(path)
		solution, iterations, n_variables, n_clauses = q_sat1.solve()
		print("He acabado")
		print("La solución: ", solution)
		print("El número de iteraciones: ", iterations)
		print("El número de variables superpuestas máximas: ", n_variables)
		print("El número de cláusulas máximas ", n_clauses)
		print("El número de qubits máximos ", q_sat1.max_qubits_grover)'''
		'''
		results =[]
		for i in range(5):
			q_sat1 = None
			print("Esto es sooooooolve")
			path = "3-sat-overleaf.dimacs"
			q_sat1 = Quantum_DSAT(path, seed=i)
			solution, iterations, n_variables, n_clauses = q_sat1.solve()
			print("He acabado")
			print("La solución: ", solution)
			print("El número de iteraciones: ", iterations)
			print("El número de variables superpuestas máximas: ", n_variables)
			print("El número de cláusulas máximas ", n_clauses)
			print("El número de qubits máximos ", q_sat1.max_qubits_grover)
			results.append({'iteraciones': iterations, 'clauses': n_clauses, 'qubits': q_sat1.max_qubits_grover, 'variables': n_variables})
		print("Iteraciones     clauses    qubits     variables")
		for result in results:
			print(result['iteraciones'], result['clauses'], result['qubits'], result['variables'])
	def test_create_arbitrary_superposition(self):
		w=[0.06364909, 0.14002801, 0.25459638, 0.95473642]
		print("Empieza la prueba arbitraria")
		q_sat = Quantum_DSAT()
		q_sat.create_arbitrary_superposition(w)
	'''
	'''def test_step_7(self):#todo
		nc1 = [[4,1],[-3],[2,-4],[5,3],[6,5,10],[11,-12],[11,13,-10],[3],[14,-16]]
		nc2 = [[4,1],[-3,-1],[4],[2,-4],[5,3],[6,5,10,-6],[3,3],[11,-12],[11,13,-10,-13],[14,15],[4,-4],[14,-16]]
		
		nc1_expected = [[4,1],[-3],[2,-4],[5,3],[6,5,10],[11,-12],[11,13,-10],[3],[14,-16]]
		nc2_expected = [[4,1],[-3,-1],[4],[2,-4],[5,3],[3,3],[11,-12],[14,15],[14,-16]]

		q_sat = Quantum_DSAT()
		
		q_sat.nc = nc1
		q_sat.step_2()
		q_sat.nc

		self.assertEqual(len(nc1_expected), len(q_sat.nc))
		for i in range(len(nc1_expected)):
			self.assertListEqual(nc1_expected[i], q_sat.nc[i])'''

