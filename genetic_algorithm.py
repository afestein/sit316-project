import time
import numpy as np
from numpy.random import randint
from numpy.random import rand

def load_csv():
    with open("data.csv") as file:
        ncols = len(file.readline().split(","))
        data = np.loadtxt(file, delimiter=",", usecols=range(1, ncols))
    return data

cities = load_csv()

def get_cost(bitstring):
    cost = 0
    for c in cities:
        stationed_city_distances = []
        for i, b in enumerate(bitstring):
            if b:
                stationed_city_distances.append(c[i])
            
        cost += np.min(stationed_city_distances)
    return cost


# tournament selection
def selection(pop, scores, k=3):
	select_idx = randint(len(pop))
	for idx in randint(0, len(pop), k-1):
		if scores[idx] < scores[select_idx]:
			select_idx = idx
	return pop[select_idx]
    

def crossover(p1, p2, crossover_rate):
	c1, c2 = p1.copy(), p2.copy()
	if rand() < crossover_rate:
        # chosen crossover point cant be on the end of the string
		c_point = randint(1, len(p1)-2)
		c1 = p1[:c_point] + p2[c_point:]
		c2 = p2[:c_point] + p1[c_point:]

	return [c1, c2]


def mutation(bitstring, mutation_rate):
    for i in range(len(bitstring)):
        if rand() < mutation_rate:
            bitstring[i] = 1-bitstring[i]

    return bitstring

def get_random_bitstring(n_bits, n_true):
    true_indices = np.random.choice(range(n_bits), size=n_true, replace=False)
    return [1 if i in true_indices else 0 for i in range(n_bits)]


def is_legal_bitstring(bitstring, n_true):
    return np.sum(bitstring) == n_true

def run_genetic_algorithm(num_generations, population_size, crossover_rate, mutation_rate, n_bits, n_true):
    population = [get_random_bitstring(n_bits, n_true) for _ in range(population_size)]
    best_solution = population[0]
    for generation in range(num_generations):
        scores = [get_cost(c) for c in population]

        for solution in population:
            if get_cost(solution) < get_cost(best_solution):
                best_solution = solution

        selected_parents = [selection(population, scores) for _ in range(population_size)]

        children = []
        for i in range(0, population_size, 2):
            parent_1, parent_2 = selected_parents[i], selected_parents[i+1]
            for child in crossover(parent_1, parent_2, crossover_rate):
                child = mutation(child, mutation_rate)
                # crossover and mutation produces many illegal results (more/less stations than required)
                # so a check is added here to ensure the new population of children only include valid solutions
                # this has the side effect of reducing the population size
                # a suitable starting population size must be chosen to obtain an optimal result (100 seems to be plenty)
                if is_legal_bitstring(child, n_true):
                    children.append(child)

        population = children

    print(f"\nBest result found from genetic algorithm: {best_solution}\ndistance: - {get_cost(best_solution)}")


if __name__ == "__main__":
    num_cities = len(cities[0])
    num_stations = 6
    start = time.time()
    run_genetic_algorithm(
        num_generations=100, 
        population_size=100, 
        crossover_rate=0.7, 
        mutation_rate=0.05, 
        n_bits=num_cities, 
        n_true=num_stations
    )
    runtime = time.time() - start
    print(f"Took {runtime:0.3f} seconds to run genetic algorithm")
 
