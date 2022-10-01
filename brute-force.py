import more_itertools
import numpy as np
import time
from utils import plot_solution

### Load city distance data ###
# Read CSV file
def load_csv():
    with open("./data/data.csv") as file:
        ncols = len(file.readline().split(","))
        data = np.loadtxt(file, delimiter=",", usecols=range(1, ncols))
    return data


cities = load_csv()
city_count = cities[0].size

print("City distances:")
for city in cities:
    print(city)

### Find all possible distinct permutations of 6 fire stations in 15 cities ###
start = time.time()
# Build a binary starting array for station distribution
station_count = 6
starting_array = ([True] * station_count) + ([False] * (city_count - station_count))

# Get all unique permutations for station locations
permutations = list(
    more_itertools.distinct_permutations(
        starting_array,
        len(starting_array),
    )
)

print("\nNumber of distinct station permutations: {}\n".format(len(permutations)))

### Brute force solution, check each possible permutation ###
optimal_distance = 1000000

for permutation in permutations:
    distances = []

    # For each city
    for i in range(city_count):
        city_distances = cities[i]
        station_distances = []

        # For each distance to each city
        for j in range(city_count):
            # If this city has a station, add it to the list of candidate station distances
            if permutation[j]:  # True or false
                station_distances.append(cities[i][j])

        # Pick the closest from the list of station distances
        closest_station_distance = np.amin(station_distances)
        distances.append(closest_station_distance)

    total_permutation_distance = sum(distances)

    if total_permutation_distance < optimal_distance:
        optimal_distance = total_permutation_distance
        optimal_permutation = permutation

print("============")
print("Optimal total distance: ", optimal_distance)
print("Optimal station locations: ", optimal_permutation)
runtime = time.time() - start
print(f"\nTook {runtime:0.3f} seconds to run brute force")

plot_solution(optimal_permutation, cities)