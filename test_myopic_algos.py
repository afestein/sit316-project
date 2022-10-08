from greedy_add import greedy_add
from greedy_drop import greedy_drop
from utils import load_csv, get_cost, print_output, output_to_csv, plot_solution
from neighbourhood_search import run_neighbourhood_search
import time

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

]

algorithms = {
	'Greedy Add':greedy_add,
	'Greedy Drop':greedy_drop
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
		
		solution, best_cost, _ = algorithm(cities, num_stations)

		runtime = time.time() - start


		n_sol, n_cost = run_neighbourhood_search(solution, cities)
		ns_runtime = time.time() - start
		
		print_output(name, runtime, best_cost, num_cities, num_stations)
		plot_solution(solution, cities, f"{filename}_{num_cities}_{num_stations}.png")

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

	output_to_csv(filename, test_results + search_results)