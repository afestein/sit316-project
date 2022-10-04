from genetic_algorithm import run_genetic_algorithm
from utils import load_csv, get_cost, print_output
import time
import numpy as np

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
	{
		'data':'100_cities.csv',
		'num_stations':40
	},
	{
		'data':'500_cities.csv',
		'num_stations':100
	},
]



for test in tests:
	cities = load_csv(f"./data/{test['data']}")
	num_stations = test['num_stations']
	num_cities = len(cities)
	start = time.time()
	best_solution, best_solutions, gen_solutions = run_genetic_algorithm(
		cities=cities,
		num_generations=100, 
		population_size=150, 
		crossover_rate=0.8, 
		mutation_rate=0.5, 
		n_bits=num_cities, 
		n_true=num_stations,
		num_elites=25,
		stuck_max=50
	)
	runtime = time.time() - start
	best_dist = get_cost(best_solution, cities, num_stations)
	print(f"Total stations: {np.sum(best_solution)}")
	print_output("Genetic Algorithm", runtime, best_dist, num_cities, num_stations)