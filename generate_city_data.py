import csv
import numpy as np

def generate_city_data(num_cities, filename, max_distance):
    fields = ['Column1']
    all_rows = []
    distances = np.random.randint(1,max_distance,size=(num_cities,num_cities))
    symm_distances = (distances + distances.T)/2

    for i in range(num_cities):
        city_name = f'City{i+1}'
        fields.append(city_name)
        for j in range(num_cities):
            symm_distances[i][j] = int(symm_distances[i][j])
            if(i == j):
                symm_distances[i][j] = 0

        row = [city_name]
        row.extend(symm_distances[i])
        all_rows.append(row)

    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(all_rows)

if __name__ == "__main__":
    num_cities = 10
    filename = f"./data/{num_cities}_cities.csv"
    max_distance = 50
    generate_city_data(num_cities, filename, max_distance)

    print(f"created {filename}")

