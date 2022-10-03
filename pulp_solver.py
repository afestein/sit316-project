from pulp import *
from utils import load_csv

# https://www.researchgate.net/publication/313795371_Optimization_of_P_Median_Problem_in_Python_Using_PuLP_Package

data = load_csv('./data/50_cities.csv')
location = [f"city{i}" for i in range(len(data))]

D = dict(zip(location, [
	dict(zip(location, data[i])) for i in range(len(data))
]))

p = 10

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
prob += sum(X[i][i] for i in location) == p

for i in location:
	prob += sum(X[i][j] for j in location) == 1

for i in location:
	for j in location:
		prob += X[i][j] <= X[j][j]


prob.solve()

print(f"Status: {LpStatus[prob.status]}")
print(f"Objective: {value(prob.objective)}")
solution = [0]*len(data)
for v in X.values():
	for i,node in enumerate(v.values()):
		if node.varValue:
			solution[i] = 1
			break

print(solution)

print(f"Cities: {len(data)}\nStations: {p}")
