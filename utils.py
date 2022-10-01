import numpy as np
from sklearn.manifold import MDS
import matplotlib.pyplot as plt
import pandas as pd

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

	print(f"Plot distance error: {100*(error/total_distance):0.2f}%")
	plt.show()


def get_random_bitstring(n_bits, n_true):
	true_indices = np.random.choice(range(n_bits), size=n_true, replace=False)
	return [1 if i in true_indices else 0 for i in range(n_bits)]


def is_legal_bitstring(bitstring, n_true):
	return np.sum(bitstring) == n_true


def get_cost(bitstring, cities):
	cost = 0
	for c in cities:
		stationed_city_distances = []
		for i, b in enumerate(bitstring):
			if b:
				stationed_city_distances.append(c[i])
			
		cost += np.min(stationed_city_distances)
	return cost
