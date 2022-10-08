from genetic_algorithm import run_genetic_algorithm
from utils import load_csv, get_cost, print_output, plot_progress, plot_solution, output_to_csv
from neighbourhood_search import run_neighbourhood_search
import time
import numpy as np
import csv

tests = [
	{
		'data':'5_cities.csv',
		'num_stations':1
	},
	{
		'data':'data.csv',
		'num_stations':6
	},
	{
		'data':'20_cities.csv',
		'num_stations':8
	},
	{
		'data':'30_cities.csv',
		'num_stations':15
	},
	{
		'data':'50_cities.csv',
		'num_stations':20
	},
	{
		'data':'75_cities.csv',
		'num_stations':15
	},
	{
		'data':'100_cities.csv',
		'num_stations':40
	},
	{
		'data':'250_cities.csv',
		'num_stations':50
	},
	{
		'data':'500_cities.csv',
		'num_stations':100
	},
]


test_results = []
search_results = []
for test in tests:
	results = []
	cities = load_csv(f"./data/{test['data']}")
	num_stations = test['num_stations']
	num_cities = len(cities)
	start = time.time()
	best_solution, best_solutions, gen_solutions = run_genetic_algorithm(
		cities=cities,
		num_generations=100, 
		population_size=200, 
		crossover_rate=0.7, 
		mutation_rate=0.5, 
		n_bits=num_cities, 
		n_true=num_stations,
		num_elites=25,
		stuck_max=100
	)
	runtime = time.time() - start

	n_sol, n_cost = run_neighbourhood_search(best_solution, cities)
	ns_runtime = time.time() - start

	best_dist = get_cost(best_solution, cities, num_stations)
	print(f"Total stations: {np.sum(best_solution)}")
	print_output("Genetic Algorithm", runtime, best_dist, num_cities, num_stations)
	solutions = [get_cost(s, cities, num_stations) for s in gen_solutions]
	plot_progress(solutions, f'genetic_{num_cities}_{num_stations}.png')
	plot_solution(best_solution, cities, f'genetic_{num_cities}_{num_stations}.png')

	test_results.append([
		f"{num_cities}/{num_stations}",
		f"{runtime:0.3f}",
		int(best_dist)
	])

	search_results.append([
		f"NS {num_cities}/{num_stations}",
		f"{ns_runtime:0.3f}",
		int(n_cost)
	])

output_to_csv("genetic", test_results+search_results)

