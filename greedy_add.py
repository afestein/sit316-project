from utils import get_cost, load_csv, plot_solution, plot_progress, print_output
import time

def greedy_add(cities, num_stations):
    bit_string = [0]*len(cities)
    cost_history = []
    for i in range(num_stations):
        best_cost = 10000000
        best_idx = -1

        for j, city in enumerate(cities):
            if bit_string[j]:
                continue
            
            _bitstring = bit_string.copy()
            _bitstring[j] = 1
            cost = get_cost(_bitstring, cities, 0)
            if cost < best_cost:
                best_cost = cost
                best_idx = j

        bit_string[best_idx] = 1
        cost_history.append(best_cost)

    return bit_string, best_cost

if __name__ == "__main__":
    cities = load_csv("./data/500_cities.csv")
    num_stations = 100
    start = time.time()
   
    solution, best_cost = greedy_add(cities, num_stations)
    
    end = time.time() - start
    print_output("Greedy Add", end, best_cost, len(cities), num_stations)
    # plot_solution(bit_string, cities)
    # plot_progress(cost_history)