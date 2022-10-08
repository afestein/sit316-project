from lowest_average_distance import lowest_avg
from median_average_distance import median_avg
from random_search import random_search
from greedy_drop import greedy_drop
from utils import load_csv, get_cost, print_output, plot_solution, output_to_csv
import time
from neighbourhood_search import run_neighbourhood_search

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
	{
		'data':'1000_cities.csv',
		'num_stations':200
	},
]

algorithms = {
	"Random Search":random_search,
	"Lowest Average":lowest_avg,
	"Median Average":median_avg
}

for name, algorithm in algorithms.items():
	test_results = []
	search_results = []
	filename = name.lower().replace(' ', '-')

	for test in tests:
		cities = load_csv(f"./data/{test['data']}")
		num_stations = test['num_stations']
		num_cities = len(cities)
		start = time.time()
		
		solution, best_cost = algorithm(cities, num_stations)

		runtime = time.time() - start


		n_sol, n_cost = run_neighbourhood_search(solution, cities)
		ns_runtime = time.time() - start

		print_output(name, runtime, best_cost, num_cities, num_stations)
		plot_solution(solution, cities, f"{filename}_{num_cities}_{num_stations}")

		test_results.append([
			f"{num_cities}/{num_stations}",
			f"{runtime:0.3f}",
			int(best_cost)
		])
		search_results.append([
			f"NS {num_cities}/{num_stations}",
			f"{ns_runtime:0.3f}",
			int(n_cost)
		])
	output_to_csv(filename, test_results+search_results)