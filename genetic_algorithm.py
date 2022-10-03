import time
import numpy as np
from numpy.random import randint
from numpy.random import rand
from utils import print_output, load_csv, plot_solution, get_cost, is_legal_bitstring, get_random_bitstring, animate_solutions,plot_progress

# tournament selection
def selection(pop, scores, k=3):
	select_idx = randint(len(pop))
	for idx in randint(0, len(pop), k-1):
		if scores[idx] < scores[select_idx]:
			select_idx = idx
	return pop[select_idx]
	

def make_legal(bitstring, n_true):
	total = np.sum(bitstring)
	while(total != n_true):
		total = np.sum(bitstring)
		idx = randint(len(bitstring))
		if total > n_true:
			if bitstring[idx]:
				bitstring[idx] = 0
		else:
			if not bitstring[idx]:
				bitstring[idx] = 1

	return bitstring

def crossover(p1, p2, crossover_rate, n_true):
	c1, c2 = p1.copy(), p2.copy()
	if rand() < crossover_rate:
		# chosen crossover point cant be on the end of the string
		c_point = randint(1, len(p1)-2)

		c1 = p1[:c_point] + p2[c_point:]
		c2 = p2[:c_point] + p1[c_point:]

		c1 = make_legal(c1, n_true)
		c2 = make_legal(c2, n_true)

	return [c1, c2]


def mutation(bitstring, mutation_rate):
	if rand() < mutation_rate:
		# bitshift the string rather than flipping a bit
		# this ensures mutation will not create illegal results if given a legal bitstring
		# rand_idx = randint(len(bitstring)-2)
		# bitstring = bitstring[rand_idx:] + bitstring[:rand_idx]

		idx_1 = randint(len(bitstring))
		idx_2 = randint(len(bitstring))
		while idx_1 == idx_2:
			idx_2 = randint(len(bitstring))
		
		if (bitstring[idx_1] and not bitstring[idx_2]) or (not bitstring[idx_1] and bitstring[idx_2]):
			tmp = bitstring[idx_1]
			bitstring[idx_1] = bitstring[idx_2]
			bitstring[idx_2] = tmp


	return bitstring


def run_genetic_algorithm(cities,num_generations, population_size, crossover_rate, mutation_rate, n_bits, n_true, stuck_max=50):
	population = [get_random_bitstring(n_bits, n_true) for _ in range(population_size)]
	best_solution = population[0]
	best_score = 10000000
	best_gen = 0
	best_solutions = []
	gen_solutions = []
	stuck_ctr = 0
	for generation in range(num_generations):
		if stuck_ctr == stuck_max:
			break
		stuck_ctr+=1
		scores = [get_cost(c, cities, n_true) for c in population]
		best_in_gen = 1000000
		best_gen_solution = population[0]
		for i, solution in enumerate(population):
			if scores[i] < best_score:
				best_gen = generation
				best_score = scores[i]
				best_solution = solution
				best_solutions.append(solution)
				stuck_ctr = 0

			if scores[i] < best_in_gen:
				best_in_gen = scores[i]
				best_gen_solution = solution

		gen_solutions.append(best_gen_solution)

		selected_parents = [selection(population, scores) for _ in range(population_size)]

		children = []
		for i in range(0, population_size, 2):
			parent_1, parent_2 = selected_parents[i], selected_parents[i+1]
			for child in crossover(parent_1, parent_2, crossover_rate, n_true):
				# child = child if is_legal_bitstring(child, n_true) else parent_1 if rand() > 0.5 else parent_2
				child = mutation(child, mutation_rate)
				children.append(child)

		population = children

	if len(best_solution) < 10:
		print(f"Best result found from genetic algorithm: \n{best_solution}")
	print(f"Found in generation {best_gen}")
	return best_solution, best_solutions, gen_solutions


if __name__ == "__main__":
	cities = load_csv("./data/100_cities.csv")
	num_cities = len(cities[0])
	num_stations = 15

	start = time.time()
	best_solution, best_solutions, gen_solutions = run_genetic_algorithm(
		cities=cities,
		num_generations=150, 
		population_size=150, 
		crossover_rate=0.76, 
		mutation_rate=0.5, 
		n_bits=num_cities, 
		n_true=num_stations
	)
	runtime = time.time() - start
	best_dist = get_cost(best_solution, cities, num_stations)
	print_output("Genetic Algorithm", runtime, best_dist, num_cities, num_stations)
	plot_solution(best_solution, cities)
	solutions = [get_cost(s, cities, num_stations) for s in gen_solutions]
	plot_progress(solutions)
	# animate_solutions(gen_solutions, cities, num_stations)


