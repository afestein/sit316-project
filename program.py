import numpy as np

# Load data from CSV file
def load_csv():
    with open("data.csv") as file:
        ncols = len(file.readline().split(","))
        data = np.loadtxt(file, delimiter=",", usecols=range(1, ncols))
    return data


distances = load_csv()

print(distances)
