import numpy as np
from utils import get_cost, load_csv, plot_solution, print_output, compare_solutions
import time
from neighbourhood_search import run_neighbourhood_search
'''
A naive algorithm for finding a solution to an uncapacitated p-median problem
Places stations in the cities with the lowest average distance from all other cities
 '''
def lowest_avg(cities, num_stations):
	averages = {}
	# find each cities average distance to all other cities
	for i, city in enumerate(cities):
		city_avg = np.average(city)
		averages[i] = city_avg
	# sort the averages
	sorted_averages = {key: val for key, val in sorted(
		averages.items(), key=lambda ele: ele[1], reverse=False)}
	# retrieve the top num_stations cities
	best = list(sorted_averages.keys())[:num_stations]
	# assign stations to each city which was identified with the lowest average distance
	sol = [1 if x in best else 0 for x in averages.keys()]

	best_cost = get_cost(sol, cities)
	return sol, best_cost

if __name__ == "__main__":
	cities = load_csv("./data/500_cities.csv")
	num_stations = 100
	start = time.time()
	solution, best_cost = lowest_avg(cities, num_stations)
	end = time.time() - start
	print_output("Lowest Average", end, best_cost, len(cities), num_stations)
	# plot_solution(solution, cities)
	n_sol, n_cost = run_neighbourhood_search(solution, cities)
	end = time.time() - start
	print_output("Lowest Average Neighbourhood Search", end, n_cost, len(cities), num_stations)

	solutions = [solution, n_sol]
	names = [f"Lowest Average - {best_cost}", f"Lowest Average Neighbourhood Search - {n_cost}"]
	compare_solutions(solutions, names, cities)
	# plot_solution(n_sol, cities)
	







