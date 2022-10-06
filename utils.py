import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import csv
import numpy as np
from sklearn.manifold import MDS
import pandas as pd

# read in a distance matrix csv and output an array of arrays
def load_csv(filename):
	with open(filename) as file:
		ncols = len(file.readline().split(","))
		data = np.loadtxt(file, delimiter=",", usecols=range(1, ncols))
	return data

# convert a distance matrix into an array of 2d points using multidimensional scaling
def get2d(distance_matrix):
	columns = [f"{i}" for i in range(len(distance_matrix[0]))]
	df = pd.DataFrame(data=distance_matrix, columns=columns)
	mds = MDS(n_components=2, dissimilarity="precomputed")
	X2d = mds.fit_transform(df)
	return X2d

# standard distance equation
def get_distance(xy1, xy2):
	return np.sqrt(((xy1[0]-xy2[0])**2) + ((xy1[1]-xy2[1])**2))

# using the best solutions obtained in each solution
# create a matplotlib animation which displays how the solution graph changed
# as the algorithm progressed
def animate_solutions(best_solutions, cities, num_stations):
	cities2d = get2d(cities)

	# initializing a figure in 
	# which the graph will be plotted
	fig = plt.figure() 
	
	# marking the x-axis and y-axis
	axis = plt.axes() 
	
	station_scat = ''
	city_scat = ''
	lines = []
	for i in range(len(cities2d)):
		c_x, c_y = zip(cities2d[i])
		if best_solutions[0][i]:
			station_scat = axis.scatter(c_x, c_y, c="red")
		else:
			city_scat = axis.scatter(c_x, c_y, c="blue")
				
		closest = 10000
		station_idx = -1

		for j, b in enumerate(best_solutions[0]):
			distance = get_distance(cities2d[i], cities2d[j])

			if b:
				if distance < closest:
					closest = distance
					station_idx = j	

		s_x, s_y = zip(cities2d[station_idx])
		lines.append(axis.plot([s_x, c_x],[s_y, c_y], color="gray", linewidth=0.5))
	
	text = axis.text(0, 0, get_cost(best_solutions[0], cities, num_stations))

	def animate(frame):
		axis.clear()
		lines = []
		for i in range(len(cities2d)):
			c_x, c_y = zip(cities2d[i])

			city_scat = axis.scatter(c_x, c_y, c="blue")

			if best_solutions[frame][i]:
				station_scat = axis.scatter(c_x, c_y, c="red")
					
			closest = 10000000
			station_idx = -1

			for j, b in enumerate(best_solutions[frame]):
				distance = get_distance(cities2d[i], cities2d[j])
		
				if b:
					if distance < closest:
						closest = distance
						station_idx = j


			s_x, s_y = zip(cities2d[station_idx])
			lines.append(axis.plot([s_x, c_x],[s_y, c_y], color="gray", linewidth=0.5))

		text = axis.text(0, 0, f"{frame}: {get_cost(best_solutions[frame], cities, num_stations)}")
		output = [station_scat, city_scat, text] + lines

		return output
	
	anim = FuncAnimation(fig, animate, frames = 200*(len(best_solutions)//100), interval=250)
	plt.show()
	# anim.save('genetic_algorithm.gif', writer = 'PillowWriter', fps = len(best_solutions)//2)

# using an array of results given by an algorithm,
# plot how the algorithm's results changed over time
def plot_progress(results, filename=None):
	fig, ax = plt.subplots() 
	ax.plot(range(len(results)), results)
	if filename:
		plt.savefig(f"./images/progress_{filename}")
	else:
		plt.show()

	fig.clear()

# plot a graph with points representing cities and stations
# plot lines between cities representing their connection to their nearest station
# in the given solution
def plot_solution(best_solution, cities, filename=None):
	cities2d = get2d(cities)

	x, y = zip(*cities2d)
	total_distance = 0
	error = 0

	fig, ax = plt.subplots() 
	for i in range(len(cities2d)):
		c_x, c_y = zip(cities2d[i])
		if best_solution[i]:
			ax.scatter(c_x, c_y, c="red")
		else:
			ax.scatter(c_x, c_y, c="blue")
				
		closest = 10000
		station_idx = -1

		for j, b in enumerate(best_solution):
			distance = get_distance(cities2d[i], cities2d[j])
			error += abs(distance - cities[i][j])
	
			if b:
				if distance < closest:
					closest = distance
					station_idx = j

			total_distance += distance	

		if station_idx != i:
			s_x, s_y = zip(cities2d[station_idx])
			ax.plot([s_x, c_x],[s_y, c_y], color="gray", linewidth=0.5)

	# print(f"Plot distance error: {100*(error/total_distance):0.2f}%")
	if filename:
		plt.savefig(f"./images/solution_{filename}")
	else:
		plt.show()

	fig.clear()
	
# returns a random bitstring of length n_bits, containing exactly n_true 1s
def get_random_bitstring(n_bits, n_true):
	true_indices = np.random.choice(range(n_bits), size=n_true, replace=False)
	return [1 if i in true_indices else 0 for i in range(n_bits)]

# determines if a given bitstring is legal for the current problem
def is_legal_bitstring(bitstring, n_true):
	return np.sum(bitstring) == n_true

# keep track of solutions and their results to improve efficiency
# if a solution is seen again, the calculation of the result can be skipped
costs = {}
def get_cost(bitstring, cities, n_true=0):
	# heavily penalize any solutions that are not legal
	if n_true and not is_legal_bitstring(bitstring, n_true):
		return 1000000000

	# Dynamic Programming addition
	_b_string = ''.join(str(x) for x in bitstring)
	if _b_string in costs:
		return costs[_b_string]
	
	cost = 0
	# iterate over all cities
	for c in cities:
		# a suitably high number
		min_dist = 10000000000
		# iterate over the provided solution bitstring
		# to find the nearest station to the current city
		# the distance from the current city to its nearest station is added to the cost value
		for i, b in enumerate(bitstring):
			if b and c[i] < min_dist:
				min_dist = c[i]

		cost += min_dist
	costs[_b_string] = cost
	return cost

def print_output(algo_name, time, best_dist, num_cities, num_stations):
    print(f"{algo_name} results")
    print(f"Time: {time:0.3f}s")
    print(f"Best distance: {best_dist}")
    print(f"Cities: {num_cities}")
    print(f"Stations: {num_stations}\n")


def output_to_csv(algo_name, data):
	HEADERS = ['cities/stations','runtime','solution', 'generations','population','crossover','mutation','elites']
	# HEADERS = ['cities/stations','runtime','solution']
	filename = f"./tests/test-{algo_name}.csv"
	with open(filename, 'w', newline="") as fn:
		csvwriter = csv.writer(fn) 
		csvwriter.writerow(HEADERS) 
		csvwriter.writerows(data)

	print(f'created {filename}')


# https://stackoverflow.com/questions/49494078/find-the-median-from-afind_weighted_median-dictionary-of-values-and-number-of-their-occurences
def get_median(item_dict : dict[int, int]) -> int:
    df = pd.DataFrame.from_dict(item_dict, orient='index').reset_index()
    df.columns = ['idx', 'distance']
    df['cum_sum'] = df['distance'].cumsum()
    total_count = df.iloc[-1, -1]
    for id, row in df.iterrows():
        if row['cum_sum'] >= int(total_count*0.5):
            return row['idx']