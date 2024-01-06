import json
import itertools

def first_fit_decreasing(orders, capacity):
    sorted_orders = sorted(orders, key=lambda x: x[1], reverse=True)
    bins = []
    for order in sorted_orders:
        placed = False
        for bin in bins:
            if sum(o[1] for o in bin) + order[1] <= capacity:
                bin.append(order)
                placed = True
                break
        if not placed:
            bins.append([order])
    return bins

def calculate_total_distance(route, dist_matrix):
    total_dist = 0
    for i in range(len(route) - 1):
        total_dist += dist_matrix[int(route[i][1:])][int(route[i+1][1:])]
    return total_dist

def find_optimal_route(slot, dist_matrix):
    min_route = None
    min_distance = float('inf')
    for perm in itertools.permutations(slot):
        current_route = ['r0'] + list(perm) + ['r0']
        current_distance = calculate_total_distance(current_route, dist_matrix)
        if current_distance < min_distance:
            min_distance = current_distance
            min_route = current_route
    return min_route

def solve_vrp(orders, dist_matrix, vehicle_capacity):
    bins = first_fit_decreasing(orders, vehicle_capacity)
    optimized_routes = {}

    for i, bin in enumerate(bins, start=1):
        slot = [n[0] for n in bin]
        optimized_route = find_optimal_route(slot, dist_matrix)
        optimized_routes[f'path{i}'] = optimized_route

    return optimized_routes

# Load the data
file_path = "Z:\Mock Hackathon\Input data\level1b.json"
with open(file_path, 'r') as file:
    data = json.load(file)

# Parse data
n_neighbourhoods = data['n_neighbourhoods']
neighborhoods = data['neighbourhoods']
restaurant_distances = data['restaurants']['r0']['neighbourhood_distance']
vehicle_capacity = data['vehicles']['v0']['capacity']

# Create distance matrix
dist_matrix = [[0] * (n_neighbourhoods + 1) for _ in range(n_neighbourhoods + 1)]
dist_matrix[0] = [0] + restaurant_distances
for i in range(n_neighbourhoods):
    dist_matrix[i + 1] = [restaurant_distances[i]] + neighborhoods[f'n{i}']['distances']


# Create orders list
orders = [(f'n{i}', neighborhoods[f'n{i}']['order_quantity']) for i in range(n_neighbourhoods)]

# Solve VRP
optimized_routes = solve_vrp(orders, dist_matrix, vehicle_capacity)

# Format and output results
output = {"v0": optimized_routes}
output_json = json.dumps(output, indent=2)
print(output_json)

# Output to a file
#with open("level1b_output.json", "w") as outfile:
    #outfile.write(output_json)
