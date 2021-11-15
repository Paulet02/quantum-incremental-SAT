import unittest
from code.util.utils import *
import os


class UtilsTest(unittest.TestCase):
	current_path = os.path.dirname(os.path.abspath(__file__))
	
	def test_variables(self):
		sat = [[4,1],[-4,3,-2],[-3,-1],[2,-4],[4,3]]
		variables_expected = [1, 2, 3, 4]
		self.assertListEqual(variables_expected, variables(sat))

	def test_literals(self):
		sat = [[4,1],[-4,3,-2],[-3,-1],[2,-4],[4,3]]
		literals_expected = [1, 2, 3, 4, -1, -4, -3, -2]
		self.assertListEqual(literals_expected, literals(sat))

	def test_iterations(self):
		self.assertEqual(round(iterations(4,1), -3), round(2.641592653589793, -3))

	def test_evaluate(self):
		conf = {1: True, -1: False, 3:True, -3:False, 4:False, -4:True, -5:False,5:True,7:False, -7:True}
		sat = [[-3, 2, 1], [-7], [-7, -2, 4], [-4, -7, -6], [-7], [5, 2], [-6, -2, -4], [5]]
		self.assertTrue(evaluate(sat,conf))

	def test_distance(self):
		self.assertEqual(distance([1,2,3],[3,7,8,9]), 1)

	def test_split_literals(self):
		normal, negate = split_literals([-7, -2, 4])
		self.assertListEqual([4], normal)
		self.assertListEqual([-7,-2], negate)

	def test_get_number_solutions(self):
		sat = [[4,1],[-4,3,-2],[-3,-1],[2,-4],[4,3]]
		self.assertEqual(1, get_number_solutions(sat))

		sat = [[-3, 2, 1], [-7], [-7, -2, 4], [-4, -7, -6], [-7], [5, 2], [-6, -2, -4], [5]]
		self.assertEqual(24, get_number_solutions(sat))

		sat = [[-1,7,2],[3,6,4]]
		self.assertEqual(49, get_number_solutions(sat))

	def test_appearances_in(self):
		appears, not_appears = appearances_in([[-7, -2, 4]], [[-4, -7, -6]])
		self.assertListEqual([4, 7], appears)
		self.assertListEqual([2], not_appears)

	def test_variables_in_clause(self):
		self.assertListEqual([1, 2, 3], variables_in_clause([-3, 2, 1]))
		self.assertListEqual([1, 2, 3, 4], variables_in_clause(list({1: False, -1: True, 2: True, -2: False, 3: True, -3: False, 4: False, -4: True}.keys())))

	def test_get_data_dimacs(self):
		n_variables, n_clauses, clauses = get_data_dimacs(str(self.current_path) + "/dimacs/tfm-sat.dimacs")
		self.assertEqual(4, n_variables)
		self.assertEqual(5, n_clauses)
		sat_expected = [[4,1],[-4,3,-2],[-1,-3],[2,-4],[4,3]]
		self.assertEqual(len(sat_expected), len(clauses))
		for i in range(len(clauses)):
			self.assertListEqual(sat_expected[i], clauses[i])
		
	def test_get_solution(self):
		sat = [[4,1],[-4,3,-2],[-1,-3],[2,-4],[4,3]]
		solution = get_solution(sat, conf={})
		solution_expected = {1: False, -1: True, 2: True, -2: False, 3: True, -3: False, 4: True, -4: False}
		self.assertDictEqual(solution_expected, solution)
		

	def test_findsubsets(self):
		elements = [1,2,3,4]
		combinations = findsubsets(elements, 3)
		solution_expected = [(1, 2, 3), (1, 2, 4), (1, 3, 4), (2, 3, 4)]
		self.assertListEqual(solution_expected, combinations)

	def test_variables_in_dict(self):
		conf = {1: False, -1: True, 2: True, -2: False, 3: True, -3: False, 4: True, -4: False}
		vars_expected = [1, 2, 3, 4]
		vars = list(variables_in_dict(conf))
		self.assertListEqual(vars_expected, vars)

		conf = {-1: True, 2: True, -2: False, 5: True, 3: True, -3: False, 4: True, -4: False}
		vars_expected = [1, 2, 3, 4, 5]
		vars = list(variables_in_dict(conf))
		self.assertListEqual(vars_expected, vars)

	def test_heuristic_sort_by_appearances(self):
		clauses = [[4,1,2],[-4,3,-2],[-4,-1,-3],[-3,2,-4],[2,4,3]]
		order = heuristic_sort_by_appearances(clauses)
		order_expected = [{'clause': [-4, 3, -2], 'distance': 0}, {'clause': [-4, -1, -3], 'distance': 0}, {'clause': [-3, 2, -4], 'distance': 0}, {'clause': [2, 4, 3], 'distance': 0}, {'clause': [4, 1, 2], 'distance': 0.22222}]

		for i in range(len(order)):
			self.assertListEqual(order_expected[i]['clause'], order[i]['clause'])
			self.assertEqual(order_expected[i]['distance'], order[i]['distance'])

'''

	def test_satisfied(self):
		conditions = {'a': [True, False, False], 'b': [True, False, False], 'c': [False, False, True]}
		self.assertTrue(utils.satisfied(conditions))

		conditions = {'a': [False, True, False], 'b': [False, False, False], 'c': [False, True, False]}
		self.assertFalse(utils.satisfied(conditions))
		
	def test_now_in_milis(self):
		self.assertEqual(round(utils.now_in_milis(), -3), round(int(time.time() * 1000), -3))
		
	def test_data_ohlcv_poloniex_to_dataframe(self):
	
		with open( str(self.current_path) + "/data/input_data_ohlcv_poloniex_to_dataframe.pickle", "rb" ) as file:
			input_data = pickle.load( file )
			
		output_data = pd.read_pickle( str(self.current_path) + "/data/output_data_ohlcv_poloniex_to_dataframe.pickle" )
		
		result = utils.data_ohlcv_poloniex_to_dataframe(input_data)
		
		pd.testing.assert_frame_equal(result, output_data)
		
	def test_calculate_VaR(self):
		with open( str(self.current_path) + "/data/input_calculate_VaR.pickle", "rb" ) as file:
			input_data = pickle.load( file )
		
		expected_result = -0.004035994172242651
		
		result = utils.calculate_VaR(input_data, 0.99)
		
		self.assertEqual(result, expected_result)
		
	def test_generate_surface_VaR(self):
		input_data = pd.read_pickle( str(self.current_path) + "/data/input_generate_surface_VaR.pickle" )
		
		with open( str(self.current_path) + "/data/output_generate_surface_VaR.pickle", "rb" ) as file:
			output_data = pickle.load( file )
		
		result = utils.generate_surface_VaR(input_data, np.arange(60*5,60*15,15), np.arange(0.90,0.995,0.001))
		
		np.testing.assert_array_equal(result, output_data)
		
	def test_get_success_percent(self):
		result = round(utils.get_success_percent(10, 30, 0.75, 0.5, 1), 8)
		self.assertEqual(result, 0.16666667)
		
		result = round(utils.get_success_percent(15, 30, 0.75, 0.5, 1), 8)
		self.assertEqual(result, 0.25)
		
		result = round(utils.get_success_percent(5, 30, 0.75, 0.5, 1), 8)
		self.assertEqual(result, 0.08333333)
		
		result_1 = round(utils.get_success_percent(10, 30, 1, 0.5, 1), 8)
		result_2 = round(utils.get_success_percent(15, 30, 1, 0.5, 1), 8)
		result_3 = round(utils.get_success_percent(5, 30, 1, 0.5, 1), 8)
		self.assertEqual(result_1 + result_2 + result_3, 1)
		
	def test_data_trades_poloniex_to_dataframe(self):
		input_data = pd.read_pickle( str(self.current_path) + "/data/input_data_trades_poloniex_to_dataframe.pickle" )
		
		with open( str(self.current_path) + "/data/output_data_trades_poloniex_to_dataframe.pickle", "rb" ) as file:
			output_data = pickle.load( file )
		
		result = utils.data_trades_poloniex_to_dataframe(input_data)
		pd.testing.assert_frame_equal(result, output_data)
		'''