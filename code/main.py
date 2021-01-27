from util.utils import *

sat = [[4,1],[-4,3,-2],[-3,-1],[2,-4],[4,3]]
#print(q_sat.get_number_solutions(sat))
#print("Orden: ",q_sat.calculate_variables_order([[4,1],[-4,3,-2],[-3,-1],[2,-4],[4,3]]))
#print(q_sat.iterations(6, 49))
sol_49 = [[-1,7,2],[3,6,4]]
#print(q_sat.create_custom_Grover({1: 2,2: 2,3:2,4:2}, [[4,1],[-4,3,-2],[-3,-1],[2,-4],[4,3]]))
#print(q_sat.create_custom_Grover({1: 2,2: 2,3:2,4:2,7:2,6:2}, sol_49))
s=[[-3, 2, 1], [-7], [-7, -2, 4], [-4, -7, -6], [-6, -2, -4],[10,-11]]
#print(q_sat.create_custom_Grover({1: 2,2: 2,3:2,4:2,6:2,7:0,10:2,11:2}, s))

print("variables: ",variables(sat))
print("literals: ",literals(sat))
bg = bin_generator(5)
for i in range(2**5):
    print(next(bg))
print(iterations(4, 1))
conf = {1: True, -1: False, 3:True, -3:False, 4:False, -4:True, -5:False,5:True,7:False, -7:True}
sat = [[-3, 2, 1], [-7], [-7, -2, 4], [-4, -7, -6], [-7], [5, 2], [-6, -2, -4], [5]]
print("L evaluacion es: ",evaluate(sat,conf))
print("La distancia es: ", distance([1,2,3],[3,7,8,9]))
print("El spllit: ", split_literals([-7, -2, 4]))
a,b=appearances_in([[-7, -2, 4]], [[-4, -7, -6]])
print("Apariencias en :", a, b)