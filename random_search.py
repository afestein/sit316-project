from utils import load_csv, plot_solution, get_cost, get_random_bitstring
import time


cities = load_csv("data/20_cities.csv")
num_cities = len(cities[0])
num_stations = 6
num_iterations = 100

start = time.time()
best_solution = get_random_bitstring(num_cities, num_stations)
for _ in range(num_iterations):
    bitstring = get_random_bitstring(num_cities, num_stations)
    if get_cost(bitstring, cities, num_stations) < get_cost(best_solution, cities, num_stations):
        best_solution = bitstring

runtime = time.time() - start

print(f"\nTook {runtime:0.3f} seconds to run random search")
print(f"Distance: {get_cost(best_solution, cities, num_stations)}")


if len(best_solution) < 10:
    print(f"Best solution found from random search: {best_solution}")

plot_solution(best_solution, cities)
