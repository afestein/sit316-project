from utils import load_csv, get_cost, plot_solution, plot_progress, print_output
import time

if __name__ == "__main__":
    cities = load_csv("./data/100_cities.csv")
    num_stations = 15
    averages = {}
    start = time.time()
    cost_history = []
    bit_string = [1]*len(cities)
    for i in range(len(cities)-num_stations):
        best_cost = 10000000
        best_idx = -1

        for j, city in enumerate(cities):
            if not bit_string[j]:
                continue
            
            _bitstring = bit_string.copy()
            _bitstring[j] = 0
            cost = get_cost(_bitstring, cities)
            if cost < best_cost:
                best_cost = cost
                best_idx = j

        bit_string[best_idx] = 0
        cost_history.append(best_cost)

    end = time.time() - start
    print_output("Greedy Drop", end, best_cost, len(cities), num_stations)
    plot_solution(bit_string, cities)
    plot_progress(cost_history)


