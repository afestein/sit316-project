import numpy as np
from utils import get_cost, load_csv, plot_solution, print_output
import time

def lowest_avg(cities, num_stations):
    averages = {}
    for i, city in enumerate(cities):
        city_avg = np.average(city)
        averages[i] = city_avg

    sorted_averages = {key: val for key, val in sorted(
        averages.items(), key=lambda ele: ele[1], reverse=False)}

    best = list(sorted_averages.keys())[:num_stations]

    sol = [1 if x in best else 0 for x in averages.keys()]

    best_cost = get_cost(sol, cities)
    return sol, best_cost

if __name__ == "__main__":
    cities = load_csv("./data/100_cities.csv")
    num_stations = 40
    start = time.time()
    solution, best_cost = lowest_avg(cities, num_stations)
    end = time.time() - start
    print_output("Lowest Average", end, best_cost, len(cities), num_stations)
    plot_solution(solution, cities)




