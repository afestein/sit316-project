from pulp_solver import run_pulp_solver
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
	filename= f"./data/{test['data']}"
	cities=load_csv(filename)
	num_cities = len(cities)
	num_stations = test['num_stations']
	start = time.time()
	best_solution, best_cost = run_pulp_solver(filename, num_stations)
	runtime = time.time() - start

	#print_output("pulp solver", runtime, best_dist, num_cities, num_stations)
	#solutions = [get_cost(s, cities, num_stations) for s in gen_solutions]
	#plot_progress(solutions, f'pulp_{num_cities}_{num_stations}.png')
	#plot_solution(best_solution, cities, f'pulp_{num_cities}_{num_stations}.png')

	test_results.append([
		f"{num_cities}/{num_stations}",
		f"{runtime:0.3f}",
		int(best_cost)
	])
output_to_csv("pulp", test_results)

