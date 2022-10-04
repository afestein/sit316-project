from greedy_add import greedy_add
from greedy_drop import greedy_drop
from utils import load_csv, get_cost, print_output
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
		'data':'50_cities.csv',
		'num_stations':20
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
	for test in tests:
		cities = load_csv(f"./data/{test['data']}")
		num_stations = test['num_stations']
		num_cities = len(cities)
		start = time.time()
		
		solution, best_cost = algorithm(cities, num_stations)

		runtime = time.time() - start

		print_output(name, runtime, best_cost, num_cities, num_stations)