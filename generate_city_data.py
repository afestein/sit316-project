import csv
import numpy as np

# generate a symmetric matrix of shape (num_cities, num_cities)
# with values between 1 and max_distance
# save this matrix into a csv file with the same format as the original problem
def generate_city_data(num_cities, filename, max_distance):
    fields = ['Column1']
    all_rows = []
    # generate a random matrix of the required size, with values limited by max_distance
    distances = np.random.randint(1,max_distance,size=(num_cities,num_cities))
    # create a symmetric matrix to be used as the distance matrix
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
    num_cities = 30
    filename = f"./data/{num_cities}_cities.csv"
    max_distance = num_cities * 2.6 # same ratio as the provided data
    generate_city_data(num_cities, filename, max_distance)

    print(f"created {filename}")

