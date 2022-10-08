import time
import numpy as np
from numpy.random import randint
from numpy.random import rand
from utils import print_output, load_csv, plot_solution, get_cost, is_legal_bitstring, get_random_bitstring, animate_solutions,plot_progress
from neighbourhood_search import run_neighbourhood_search
# allow the top num_elites of the population to survive to the next generation
def get_elites(population, scores, num_elites):
	sorted_scores = [index for index, num in sorted(enumerate(scores), key=lambda x: x[-1])]
	elites = []
	for idx in sorted_scores:
		if len(elites) == num_elites:
			break
		
		elites.append(population[idx])
	return elites

# tournament selection, between k members of the population
def selection(pop, scores, generation, k=10):
	select_idx = randint(len(pop))
	total_score_difference = 0
	for idx in randint(0, len(pop), k-1):
		total_score_difference = abs(scores[idx] - scores[idx-1])
		if total_score_difference < 100:
			idx =randint(0, len(pop))
		if scores[idx] < scores[select_idx]:
			select_idx = idx


		# print(total_score_difference)
	return pop[select_idx]
	
# crossover is like to produce illegal offspring
# so this function is used to "fix" the illegal solutions produced by the crossover function
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

# combine two parent solutions by picking a random point and cutting and pasting each together
# to create two children solutions
# ensure these children are legal solutions by enforcing the make_legal function
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

# randomly swap bits in the result, in a way that ensures only legal solutions are produced
def mutation(bitstring, mutation_rate):
	if rand() < mutation_rate:
		idx_1 = randint(len(bitstring))
		idx_2 = randint(len(bitstring))

		# only swap the bits if it doesn't affect the total sum of the bitstring
		if (bitstring[idx_1] and not bitstring[idx_2]) or (not bitstring[idx_1] and bitstring[idx_2]):
			tmp = bitstring[idx_1]
			bitstring[idx_1] = bitstring[idx_2]
			bitstring[idx_2] = tmp

	return bitstring


def run_genetic_algorithm(cities,num_generations, population_size, crossover_rate, mutation_rate, n_bits, n_true, num_elites=10, stuck_max=50):
	# create the initial population
	population = [get_random_bitstring(n_bits, n_true) for _ in range(population_size)]
	best_solution = population[0]
	# a suitably high number that can be beaten in the first iteration
	best_score = 10000000
	best_gen = 0
	best_solutions = []
	gen_solutions = []
	stuck_ctr = 0
	for generation in range(num_generations):
		# end the algorithm if it hasn't had any improvement for stuck_max iterations
		if stuck_ctr == stuck_max:
			break
		stuck_ctr+=1
		# get the cost of all solutions in the population
		scores = [get_cost(c, cities, n_true) for c in population]
		best_in_gen = 1000000
		best_gen_solution = population[0]
		# find the best solution from the generation
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
		# allocate some elites from the population to survive with their genes intact
		selected_parents = get_elites(population, scores, num_elites)
		# select parents from the population using tournament selection
		
		selected_parents += [selection(population, scores, generation) for _ in range(population_size-num_elites) ]

		children = []
		for i in range(0, len(selected_parents), 2):
			parent_1, parent_2 = selected_parents[i], selected_parents[i+1]
			# create new children from parents using crossover
			for child in crossover(parent_1, parent_2, crossover_rate, n_true):
				# randomly flip bits in the child solution
				child = mutation(child, mutation_rate)
				children.append(child)

		population = children

	# if len(best_solution) < 10:
	# 	print(f"Best result found from genetic algorithm: \n{best_solution}")
	# print(f"Found in generation {best_gen}")
	return best_solution, best_solutions, gen_solutions


if __name__ == "__main__":
	cities = load_csv("./data/100_cities.csv")
	num_cities = len(cities[0])
	num_stations = 40

	start = time.time()
	best_solution, best_solutions, gen_solutions = run_genetic_algorithm(
		cities=cities,
		num_generations=300, 
		population_size=100, 
		crossover_rate=0.8, 
		mutation_rate=0.5, 
		n_bits=num_cities, 
		n_true=num_stations,
		num_elites=20,
		stuck_max=100
	)
	runtime = time.time() - start
	best_dist = get_cost(best_solution, cities, num_stations)
	print_output("Genetic Algorithm", runtime, best_dist, num_cities, num_stations)
	n_sol, n_cost = run_neighbourhood_search(best_solution, cities)
	end = time.time() - start
	print_output("Genetic Algorithm Neighbourhood Search", end, n_cost, len(cities), num_stations)
	



	# print(np.sum(best_solution))
	# plot_solution(best_solution, cities)
	# solutions = [get_cost(s, cities, num_stations) for s in gen_solutions]
	# plot_progress(solutions)
	# animate_solutions(gen_solutions, cities, num_stations)


