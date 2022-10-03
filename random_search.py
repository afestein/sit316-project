from utils import load_csv, plot_solution, get_cost, get_random_bitstring, animate_solutions,plot_progress, print_output
import time


cities = load_csv("data/100_cities.csv")
num_cities = len(cities[0])
num_stations = 10
num_iterations = 200

start = time.time()
best_solution = get_random_bitstring(num_cities, num_stations)
best_result = 100000000
best_solutions = []
for _ in range(num_iterations):
    bitstring = get_random_bitstring(num_cities, num_stations)
    result = get_cost(bitstring, cities, num_stations)
    if result < best_result:
        best_result = result
        best_solution = bitstring

        best_solutions.append(bitstring)

runtime = time.time() - start
best_dist = get_cost(best_solution, cities, num_stations) 
print_output("Random Search", runtime, best_dist, len(cities), num_stations)


#animate_solutions(best_solutions, cities, num_stations)
solutions = [get_cost(s, cities, num_stations) for s in best_solutions]
plot_progress(solutions)
