from utils import get_cost, load_csv, plot_solution, plot_progress, print_output, compare_solutions
import time
from neighbourhood_search import run_neighbourhood_search
'''
The myopic greedy add algorithm for finding a solution for an uncapacitated p-median problem
A bitstring is initialized to represent no cities being assigned stations
A loop is started that runs for a number of times equal to the number of required stations.
For each iteration, all cities are then iterated over.
In each iteration of the inner loop, the cost function is checked to see if assigning a station to the current city improves it.
The city which has the greatest impact on the cost function after being assigned a station is added to the main solution
After the outer loop has run num_stations times, there will now be num_stations cities with stations assigned
'''
def greedy_add(cities, num_stations):
	# initialize a bitstring representing no stations in any cities
	bit_string = [0]*len(cities)
	# used to plot progress of the algorithm
	cost_history = []
	# loop for each required station
	for i in range(num_stations):
		best_cost = 10000000
		best_idx = -1

		for j, city in enumerate(cities):
			# skip cities that have already been assigned stations
			if bit_string[j]:
				continue
			
			# assign the current city a station and check to see if it is the best seen so far
			_bitstring = bit_string.copy()
			_bitstring[j] = 1
			cost = get_cost(_bitstring, cities, 0)
			if cost < best_cost:
				best_cost = cost
				best_idx = j
		# assign the city which had the greatest impact on the cost function a station and continue looping
		# until the required amount of stations have been assigned to cities
		bit_string[best_idx] = 1
		cost_history.append(best_cost)

	return bit_string, best_cost, cost_history





if __name__ == "__main__":
	cities = load_csv("./data/100_cities.csv")
	num_stations = 40
	start = time.time()
   
	solution, best_cost, cost_history = greedy_add(cities, num_stations)
	
	end = time.time() - start
	print_output("Greedy Add", end, best_cost, len(cities), num_stations)

	n_sol, n_cost = run_neighbourhood_search(solution, cities)
	end = time.time() - start
	print_output("Greedy Add Neighbourhood Search", end, n_cost, len(cities), num_stations)

	# plot_solution(bit_string, cities)
	# plot_progress(cost_history)
	solutions = [solution, n_sol]
	names = [f"Greedy Add - {best_cost}", f"Greedy Add Neighbourhood Search - {n_cost}"]
	compare_solutions(solutions, names, cities)