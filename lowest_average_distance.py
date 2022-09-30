import numpy as np

def get_cost(bitstring):
    cost = 0
    for c in cities:
        stationed_city_distances = []
        for i, b in enumerate(bitstring):
            if b:
                stationed_city_distances.append(c[i])

        cost += np.min(stationed_city_distances)
    return cost

def load_csv():
    with open("data.csv") as file:
        ncols = len(file.readline().split(","))
        data = np.loadtxt(file, delimiter=",", usecols=range(1, ncols))
    return data

if __name__ == "__main__":
    cities = load_csv()
    averages = {}

    for i, city in enumerate(cities):
        city_avg = np.average(city)
        averages[i] = city_avg

    sorted_averages = {key: val for key, val in sorted(
        averages.items(), key=lambda ele: ele[1], reverse=True)}

    best = list(sorted_averages.keys())[:6]

    sol = [1 if x in best else 0 for x in averages.keys()]
    print("Naive result by placing stations in cities with lowest average distance to all others")
    print(sol)
    print(get_cost(sol))


