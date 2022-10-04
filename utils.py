import numpy as np
from sklearn.manifold import MDS
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation

def load_csv(filename):
	with open(filename) as file:
		ncols = len(file.readline().split(","))
		data = np.loadtxt(file, delimiter=",", usecols=range(1, ncols))
	return data


def get2d(distance_matrix):
	columns = [f"{i}" for i in range(len(distance_matrix[0]))]
	df = pd.DataFrame(data=distance_matrix, columns=columns)
	mds = MDS(n_components=2, dissimilarity="precomputed")
	X2d = mds.fit_transform(df)
	return X2d


def get_distance(xy1, xy2):
	return np.sqrt(((xy1[0]-xy2[0])**2) + ((xy1[1]-xy2[1])**2))

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


def plot_progress(solutions):
	plt.plot(range(len(solutions)), solutions)
	plt.show()

def plot_solution(best_solution, cities):
	cities2d = get2d(cities)

	x, y = zip(*cities2d)
	total_distance = 0
	error = 0
	for i in range(len(cities2d)):
		c_x, c_y = zip(cities2d[i])
		if best_solution[i]:
			plt.scatter(c_x, c_y, c="red")
		else:
			plt.scatter(c_x, c_y, c="blue")
				
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
			plt.plot([s_x, c_x],[s_y, c_y], color="gray", linewidth=0.5)

	# print(f"Plot distance error: {100*(error/total_distance):0.2f}%")
	plt.show()


def get_random_bitstring(n_bits, n_true):
	true_indices = np.random.choice(range(n_bits), size=n_true, replace=False)
	return [1 if i in true_indices else 0 for i in range(n_bits)]


def is_legal_bitstring(bitstring, n_true):
	return np.sum(bitstring) == n_true

costs = {}
def get_cost(bitstring, cities, n_true=0):
	if n_true and not is_legal_bitstring(bitstring, n_true):
		return 1000000000

	_b_string = ''.join(str(x) for x in bitstring)
	if _b_string in costs:
		return costs[_b_string]
	
	cost = 0
	# number of cities * number of cities
	for c in cities:
		min_dist = 100000000000
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