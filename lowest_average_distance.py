import numpy as np
from utils import get_cost, load_csv, plot_solution

if __name__ == "__main__":
    cities = load_csv("./data/data.csv")
    num_stations = 6
    averages = {}

    for i, city in enumerate(cities):
        city_avg = np.average(city)
        averages[i] = city_avg

    sorted_averages = {key: val for key, val in sorted(
        averages.items(), key=lambda ele: ele[1], reverse=True)}

    best = list(sorted_averages.keys())[:num_stations]

    sol = [1 if x in best else 0 for x in averages.keys()]

    print("Naive result by placing stations in cities with lowest average distance to all others")
    print(f"Best distance: {get_cost(sol, cities)}")

    plot_solution(sol, cities)




