from utils import get_cost
import numpy as np


# Constructs a data structure that represents which cities are connected to which stations
def create_graph(solution, cities):
	graph = {}
	for i, city in enumerate(cities):
		closest = 10000
		station_idx = -1
		for j, b in enumerate(solution):
			if b:
				distance = cities[i][j]
				if distance < closest:
					closest = distance
					station_idx = j

		c_name = i	
		s_name = station_idx
		if s_name in graph:
			graph[s_name].append(c_name)
		else:
			graph[s_name] = [c_name]

	return graph

# traverses a graph and tests if a better solution can be found by placing a station
# at a different city in its neighbourhood
# the neighbourhood is defined as the cities being served by a single station
def search(graph, solution, cities):
	best_cost = get_cost(solution, cities)
	best_solution = solution.copy()
	num_cities = np.sum(solution)
	for station, connections in graph.items():
		_best_solution = best_solution.copy()
		for city in connections:
			if station == city:
				continue

			_solution = best_solution.copy()
			_solution[station] = 0
			_solution[city] = 1
			if(np.sum(_solution) > num_cities):
				print('bad solution!')

			cost = get_cost(_solution, cities)
			if cost < best_cost:
				best_cost = cost
				_best_solution = _solution.copy()

		best_solution = _best_solution.copy()
	return best_solution

# creates a graph to represent how cities are connected to stations
# searches through this graph to find better solutions by placing stations in different cities in the neighbourhoods
# if the solution has been changed from the search, it recreates the graph and searches again using the new neighbourhoods
# this process repeats until the solution is left unchanged after a search is performed
def run_neighbourhood_search(solution, cities):
	graph = create_graph(solution, cities)
	best_solution = search(graph, solution, cities)
	ctr = 0
	last_solution = solution
	while ctr < 100:
		ctr +=1
		graph = create_graph(best_solution, cities)
		best_solution = search(graph, best_solution, cities)
		if best_solution == last_solution:
			break
		
		last_solution = best_solution

	if ctr == 100:
		print("broke from counter")

	best_cost = get_cost(best_solution, cities)
	return best_solution, best_cost