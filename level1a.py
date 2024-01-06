import json

def calculate_total_distance(slot_path, distances):
    total_distance = 0
    for i in range(len(slot_path) - 1):
        node1 = slot_path[i]
        node2 = slot_path[i + 1]
        
        # Skip order quantity nodes
        if isinstance(node1, str) and isinstance(node2, str):
            total_distance += distances[node1]['distances'][int(node2[1:])]

    return total_distance

def nearest_neighbor(distances, start_node, visited_nodes):
    unvisited_nodes = set(distances.keys()) - visited_nodes
    unvisited_nodes.remove(start_node)
    current_node = start_node
    path = [current_node]

    while unvisited_nodes:
        nearest_node = min(unvisited_nodes, key=lambda x: distances[current_node]['distances'][int(x[1:])])
        path.append(nearest_node)
        unvisited_nodes.remove(nearest_node)
        current_node = nearest_node

    return path

def find_optimal_starting_point(neighbourhood_distances, visited_nodes):
    min_total_distance = float('inf')
    optimal_start_node = None

    for start_node in neighbourhood_distances.keys():
        if start_node not in visited_nodes:
            path = nearest_neighbor(neighbourhood_distances, start_node, visited_nodes)
            total_distance = calculate_total_distance(path, neighbourhood_distances)

            if total_distance < min_total_distance:
                min_total_distance = total_distance
                optimal_start_node = start_node

    return optimal_start_node

def generate_delivery_slots(neighbourhoods, distances, capacity):
    unvisited_neighbourhoods = set(neighbourhoods.keys())
    visited_nodes = set()
    current_node = None

    while unvisited_neighbourhoods:
        optimal_start_node = find_optimal_starting_point(neighbourhoods, visited_nodes)
        if current_node is not None:
            visited_nodes.add(current_node)
        unvisited_neighbourhoods.remove(optimal_start_node)
        current_node = optimal_start_node

        current_capacity = 0
        current_slot = [current_node]

        while unvisited_neighbourhoods:
            nearest_node = min(unvisited_neighbourhoods, key=lambda x: distances[current_node]['distances'][int(x[1:])])
            order_quantity = int(neighbourhoods[nearest_node]["order_quantity"])  # Convert to integer

            if current_capacity + order_quantity <= capacity:
                current_slot.append(nearest_node)
                current_capacity = current_capacity + order_quantity
                print(f"Added {nearest_node} to the current slot. Current capacity: {current_capacity}")
            else:
                yield {"path": current_slot,
                       "total_capacity": current_capacity,
                       "total_distance": calculate_total_distance(current_slot, distances)}

                current_slot = [nearest_node]
                current_capacity = order_quantity
                print(f"Starting a new slot with {nearest_node}. Current capacity: {current_capacity}")


            unvisited_neighbourhoods.remove(nearest_node)
            current_node = nearest_node

        yield {"path": current_slot,
               "total_capacity": current_capacity,
               "total_distance": calculate_total_distance(current_slot, distances)}

def main():
    with open('Input data/level1a.json') as file:
        data = json.load(file)

    neighbourhood_distances = data['neighbourhoods']

    vehicle_capacity = data['vehicles']['v0']['capacity']
    delivery_slots = list(generate_delivery_slots(data['neighbourhoods'], neighbourhood_distances, vehicle_capacity))

    output = {"v0": {}}
    for i, slot in enumerate(delivery_slots):
        path_key = f"path{i + 1}"
        output["v0"][path_key] = slot

    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()