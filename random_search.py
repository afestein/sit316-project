from utils import load_csv, plot_solution, get_cost, get_random_bitstring, animate_solutions,plot_progress, print_output
import time


# iterate for a given number of times
# foreach iteration, generate a new random solution. 
# determine its cost and hold onto it if it is the best solution seen so far
def random_search(cities, num_stations, num_iterations=500):
    num_cities = len(cities)
    best_solution = get_random_bitstring(num_cities, num_stations)
    best_result = 100000000
    for _ in range(num_iterations):
        bitstring = get_random_bitstring(num_cities, num_stations)
        result = get_cost(bitstring, cities, num_stations)
        if result < best_result:
            best_result = result
            best_solution = bitstring

    return best_solution, best_result


if __name__ == "__main__":
    cities = load_csv("data/1000_cities.csv")
    num_stations = 100
    num_iterations = 500

    start = time.time()
    best_solution, best_result = random_search(cities, num_stations, num_iterations)
    runtime = time.time() - start
    print_output("Random Search", runtime, best_result, len(cities), num_stations)


    #animate_solutions(best_solutions, cities, num_stations)
    # solutions = [get_cost(s, cities, num_stations) for s in best_solutions]
    # plot_progress(solutions)
