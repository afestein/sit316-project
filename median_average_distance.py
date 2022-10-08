import numpy as np
from utils import get_cost, load_csv, plot_solution, print_output, get_median, compare_solutions
import time
from neighbourhood_search import run_neighbourhood_search

def median_avg(cities, num_stations):
	averages = {}
	for i, city in enumerate(cities):
		city_avg = np.average(city)
		averages[i] = city_avg


	sorted_avgs = {key: val for key, val in sorted(
		averages.items(), key=lambda ele: ele[1], reverse=False)}

	medians = []
	for key, val in list(sorted_avgs.items())[:num_stations//4]:
		medians.append(key)
		del sorted_avgs[key]

	while len(medians) < num_stations:
		median = get_median(sorted_avgs)
		medians.append(median)

		del sorted_avgs[median]
		
	sol = [1 if x in medians else 0 for x in averages.keys()]

	best_cost = get_cost(sol, cities)

	return sol, best_cost


if __name__ == "__main__":

	cities = load_csv("./data/500_cities.csv")

	num_stations = 100

	start = time.time()

	solution, best_cost = median_avg(cities, num_stations)

	end = time.time() - start

	print_output("Median Average", end, best_cost, len(cities), num_stations)
	# plot_solution(solution, cities)

	n_sol, n_cost = run_neighbourhood_search(solution, cities)
	end = time.time() - start
	print_output("Median Average Neighbourhood Search", end, n_cost, len(cities), num_stations)
	solutions = [solution, n_sol]
	names = [f"Median Average - {best_cost}", f"Median Average Neighbourhood Search -{n_cost}"]
	compare_solutions(solutions, names, cities)
	# plot_solution(n_sol, cities)





