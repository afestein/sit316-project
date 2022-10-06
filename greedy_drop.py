from utils import load_csv, get_cost, plot_solution, plot_progress, print_output
import time

'''
The myopic greedy drop algorithm for finding a solution for an uncapacitated p-median problem
Stations are assigned to all cities, 
and then iterated over number of times equal to the number of cities minus the number of required stations
In each iteration, we find what city has the biggest impact on the cost function when its station is removed.
This is done by iterating over all cities again, each iteration the cost function is checked to see if it has improved since removing the station in the current city
The top loop stops after num_cities-num_stations iterations, as there will now be num_station cities remaining with stations
'''
def greedy_drop(cities, num_stations):
    # used for plotting the algorithm progress
    cost_history = []
    # create a bit string representing all cities being assigned stations
    bit_string = [1]*len(cities)
    # iterate a number of times that leaves num_stations cities with stations
    for i in range(len(cities)-num_stations):
        # a suitably high value to initialize the best_cost tracking
        best_cost = 1000000
        # initialize a variable to keep track of the index of the best_cost city
        best_idx = -1

        # iterate over all cities
        for j, city in enumerate(cities):
            # if this city doesn't have a station, it can be skipped
            if not bit_string[j]:
                continue
            # create a copy of the main bitstring and remove the station from the current city
            # then check the cost of the new solution that has no station in this city
            # if it is better than any seen so far, set it as the new best
            _bitstring = bit_string.copy()
            _bitstring[j] = 0
            cost = get_cost(_bitstring, cities)
            if cost < best_cost:
                best_cost = cost
                best_idx = j
        # update the main solution to include the best result found from iterating over the cities
        bit_string[best_idx] = 0
        cost_history.append(best_cost)

    return bit_string, best_cost, cost_history

if __name__ == "__main__":
    cities = load_csv("./data/data.csv")
    num_stations = 6

    start = time.time()
    solution, best_cost, cost_history = greedy_drop(cities, num_stations)
    end = time.time() - start
    print_output("Greedy Drop", end, best_cost, len(cities), num_stations)
    # plot_solution(bit_string, cities)
    plot_progress(cost_history)


