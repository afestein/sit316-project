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
print(cities)


def getCost(bitstring):
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
	selection_ix = randint(len(pop))
	for ix in randint(0, len(pop), k-1):
		if scores[ix] < scores[selection_ix]:
			selection_ix = ix
	return pop[selection_ix]
    

def crossover(p1, p2, crossover_rate):
	c1, c2 = p1.copy(), p2.copy()
	if rand() < crossover_rate:
		# select crossover point that is not on the end of the string
		c_point = randint(1, len(p1)-2)
		c1 = p1[:c_point] + p2[c_point:]
		c2 = p2[:c_point] + p1[c_point:]

	return [c1, c2]


def mutation(bitstring, mutation_rate):
    for i in range(len(bitstring)):
        if rand() < mutation_rate:
            bitstring[i] = 1-bitstring[i]

    return bitstring

def getRandomBitString(num_bits=15, num_true=6):
    true_indices = np.random.choice(range(num_bits), size=num_true, replace=False)
    return [1 if i in true_indices else 0 for i in range(num_bits)]


def isLegal(bitstring):
    return np.sum(bitstring) == 6

def runGeneticAlgorithm(num_generations, population_size, crossover_rate, mutation_rate, n_bits = 15):
    population = [getRandomBitString() for _ in range(population_size)]
    best_solution = population[0]
    for generation in range(num_generations):
        scores = [getCost(c) for c in population]

        for solution in population:
            if getCost(solution) < getCost(best_solution):
                best_solution = solution

        selected_parents = [selection(population, scores) for _ in range(population_size)]

        children = []
        for i in range(0, population_size, 2):
            parent_1, parent_2 = selected_parents[i], selected_parents[i+1]
            for child in crossover(parent_1, parent_2, crossover_rate):
                child = mutation(child, mutation_rate)
                # this method produces many illegal results (more/less stations than required)
                # so add a check here to ensure the new population of children only include valid solutions
                if isLegal(child):
                    children.append(child)

        population = children

    print(f"\nBest result found from genetic algorithm: {best_solution}\ndistance: - {getCost(best_solution)}")


if __name__ == "__main__":
    start = time.time()
    runGeneticAlgorithm(num_generations=100, population_size=100, crossover_rate=0.7, mutation_rate=0.05)
    runtime = time.time() - start
    print(f"Took {runtime:0.3f} seconds to run genetic algorithm")


    
