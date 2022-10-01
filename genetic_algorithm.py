import time
import numpy as np
from numpy.random import randint
from numpy.random import rand
from utils import load_csv, plot_solution, get_cost, is_legal_bitstring, get_random_bitstring

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
			# bitshift the string rather than flipping a bit
			# this ensures mutation will not create illegal results if given a legal bitstring
			rand_idx = randint(len(bitstring))
			bitstring = bitstring[rand_idx:] + bitstring[:rand_idx]

	return bitstring


def run_genetic_algorithm(cities,num_generations, population_size, crossover_rate, mutation_rate, n_bits, n_true):
	population = [get_random_bitstring(n_bits, n_true) for _ in range(population_size)]
	best_solution = population[0]
	best_score = 1000
	best_gen = 0
	for generation in range(num_generations):
		scores = [get_cost(c, cities) for c in population]

		for i, solution in enumerate(population):
			if scores[i] < best_score:
				best_gen = generation
				best_score = scores[i]
				best_solution = solution

		selected_parents = [selection(population, scores) for _ in range(population_size)]

		children = []
		for i in range(0, population_size, 2):
			parent_1, parent_2 = selected_parents[i], selected_parents[i+1]
			for child in crossover(parent_1, parent_2, crossover_rate):
				child = child if is_legal_bitstring(child, n_true) else parent_1 if rand() > 0.5 else parent_2
				child = mutation(child, mutation_rate)
				children.append(child)

		population = children

	if len(best_solution) < 10:
		print(f"\nBest result found from genetic algorithm: {best_solution}")
	print(f"Distance: {get_cost(best_solution, cities)}")
	print(f"Found in gen {best_gen}")
	return best_solution


if __name__ == "__main__":
	cities = load_csv("./data/5_cities.csv")
	num_cities = len(cities[0])
	num_stations = 1

	start = time.time()
	best_solution = run_genetic_algorithm(
		cities=cities,
		num_generations=25, 
		population_size=50, 
		crossover_rate=0.7, 
		mutation_rate=0.05, 
		n_bits=num_cities, 
		n_true=num_stations
	)
	runtime = time.time() - start
	print(f"Took {runtime:0.3f} seconds to run genetic algorithm")

	plot_solution(best_solution, cities)

