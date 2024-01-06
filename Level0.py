import networkx as nx
import json

def solve_tsp(distances):
    G = nx.Graph()

    # Add edges to the graph
    for i in range(len(distances)):
        for j in range(i + 1, len(distances[i])):
            G.add_edge(f"n{i}", f"n{j}", weight=distances[i][j])
    tsp_path = nx.approximation.traveling_salesman_problem(G, cycle=True)

    return tsp_path


f = open('Z:\Mock Hackathon\Input data\level0.json')
data = json.load(f)

neighbourhood_distances = []
for neighbourhood, info in data["neighbourhoods"].items():
    n_distances = info["distances"]
    neighbourhood_distances.append(n_distances)       
#print(neighbourhood_distances)
tsp_path = solve_tsp(neighbourhood_distances)

print("Recommended Path:")
print(" -> ".join(map(str, tsp_path)))

output_data = {
    "recommended_path": list(map(str, tsp_path))
}
with open("recommended.json", "w") as json_file:
    json.dump(output_data, json_file, indent=2)

print("Recommended path has been saved to 'recommended_path.json'")