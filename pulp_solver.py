from pulp import *
from utils import load_csv, get_cost, plot_solution
import time

# https://www.researchgate.net/publication/313795371_Optimization_of_P_Median_Problem_in_Python_Using_PuLP_Package
def run_pulp_solver(filename, num_stations):

	data = load_csv(filename)
	location = [f"city{i}" for i in range(len(data))]

	D = dict(zip(location, [
		dict(zip(location, data[i])) for i in range(len(data))
	]))

	p = num_stations

	X = LpVariable.dicts(
		f'X_{location}_{location}', 
		(location, location),
		cat='Binary',
		lowBound=0,
		upBound=1
	)

	# define minimization problem
	prob = LpProblem('P Median', LpMinimize)

	# objective function
	prob += sum(sum(D[i][j] * X[i][j] for j in location) for i in location)

	# constraints

	# solutions must have p stations
	prob += sum(X[i][i] for i in location) == p

	# each city must be assigned to exactly one station
	for i in location:
		prob += sum(X[i][j] for j in location) == 1

	# if a city i is assigned to a station at city j
	# city j must contain a station
	for i in location:
		for j in location:
			prob += X[i][j] <= X[j][j]

	start = time.time()
	prob.solve()
	runtime = time.time() - start
	print(f"Status: {LpStatus[prob.status]}")
	print(f"Objective: {value(prob.objective)}")
	solution = [0]*len(data)
	for v in X.values():
		for i,node in enumerate(v.values()):
			if node.varValue:
				solution[i] = 1
				break

	print(solution)
	best_cost = get_cost(solution, data, p)
	print(f"Cities: {len(data)}\nStations: {p}")
	return solution, best_cost
	#plot_solution(solution, data, f"pulp_{len(data)}_{p}.png")
	#with open('./tests/test-pulp.csv', 'a+', newline="") as fn:
	#	fn.write(f"{len(data)}/{p}, {runtime:0.3f},  {best_cost}\n")