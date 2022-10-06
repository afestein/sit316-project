from genetic_algorithm import run_genetic_algorithm
from utils import load_csv, get_cost, print_output, plot_progress, plot_solution, output_to_csv
import time
import numpy as np
import csv
import random

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
		'data':'50_cities.csv',
		'num_stations':20
	},
	# {
	# 	'data':'100_cities.csv',
	# 	'num_stations':40
	# },
	# {
	# 	'data':'500_cities.csv',
	# 	'num_stations':100
	# },
]

test_runs = 50
test_ctr = 0

while test_ctr < test_runs:
	print(test_ctr)
	test_results = []
	test_ctr +=1

	num_generations = random.randint(50, 400)
	population_size = random.choice(range(50, 400, 2))
	crossover_rate = random.uniform(0, 1)
	mutation_rate = random.uniform(0, 1)
	num_elites = random.randint(0, population_size)


	for test in tests:
		results = []
		cities = load_csv(f"./data/{test['data']}")
		num_stations = test['num_stations']
		num_cities = len(cities)
		start = time.time()
		best_solution, best_solutions, gen_solutions = run_genetic_algorithm(
			cities=cities,
			num_generations=num_generations, 
			population_size=population_size, 
			crossover_rate=crossover_rate, 
			mutation_rate=mutation_rate, 
			n_bits=num_cities, 
			n_true=num_stations,
			num_elites=num_elites,
			stuck_max=100
		)
		runtime = time.time() - start


		best_dist = get_cost(best_solution, cities, num_stations)
		# print(f"Total stations: {np.sum(best_solution)}")
		# print_output("Genetic Algorithm", runtime, best_dist, num_cities, num_stations)
		# solutions = [get_cost(s, cities, num_stations) for s in gen_solutions]
		# plot_progress(solutions, f'genetic_{num_cities}_{num_stations}.png')
		# plot_solution(best_solution, cities, f'genetic_{num_cities}_{num_stations}.png')

		test_results.append([
			f"{num_cities}/{num_stations}",
			f"{runtime:0.3f}",
			int(best_dist),
			num_generations,
			population_size,
			f"{crossover_rate:0.3f}",
			f"{mutation_rate:0.3f}",
			num_elites,
		])

	output_to_csv(f"genetic-{test_ctr}", test_results)

