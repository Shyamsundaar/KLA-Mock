import json

f = open('Z:\Mock Hackathon\Input data\level0.json')
data = json.load(f)

#for i in data['neighbourhoods']['n0']['distances']:
#	print(i)

neighbourhood_distances = []
visited_nodes = []
path = []

'''for neighbourhood, info in data["neighbourhoods"].items():
    n_distances = info["distances"]
    #print(f"Neighbourhood {neighbourhood}:")
    for index, distance in enumerate(n_distances):
        i = 0
        #print(f"  Distance to n{index}: {distance}")
        neighbourhood_distances[i].append(n_distances)
        i = i + 1'''

neighbourhood_distances = []

# Iterating through neighbourhoods and their distances
for neighbourhood, info in data["neighbourhoods"].items():
    n_distances = info["distances"]
    neighbourhood_distances.append(n_distances)       
#print(neighbourhood_distances)

min_distance = 13
visited_nodes.append(13)
enetred_node = []

#while len(path) != 20:
for i in neighbourhood_distances[min_distance]:
    if i>0:
        enetred_node.append(i)
    visited_nodes.append(min_distance)
	print(min(enetred_node))
print(min_distance)

f.close()
