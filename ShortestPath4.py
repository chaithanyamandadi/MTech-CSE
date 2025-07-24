import pandas as pd
import networkx as nx
import time
import math

# Step 1: Load Data
file_path = 'hyderabad_road_network_with_traffic - 50.xlsx'  # Adjust this as needed
data = pd.read_excel(file_path)

# Data Cleaning: Skip the first two rows, reset index, and rename columns
data_cleaned = data.iloc[2:].reset_index(drop=True)
data_cleaned.columns = ['source_place', 'destination_place', 'traffic_level', 'traffic_density',
                        'duration_in_traffic_seconds', 'distance_meters']

# Step 2: Graph Construction
G = nx.Graph()
for index, row in data_cleaned.iterrows():
    source = row['source_place']
    destination = row['destination_place']
    weight = row['distance_meters']  # We can also use 'distance_meters' if preferred

    # Add both directions (bidirectional roads)
    G.add_edge(source, destination, weight=weight)
    G.add_edge(destination, source, weight=weight)


# Step 3: Implementing Dijkstra's Algorithm
def dijkstra_algorithm(graph, source):
    start_time = time.time()
    length, path = nx.single_source_dijkstra(graph, source, weight='weight')
    end_time = time.time()
    execution_time = end_time - start_time
    return length, path, execution_time


# Run Dijkstra's Algorithm for "Charminar"
source_location = "Charminar"
dijkstra_lengths, dijkstra_paths, dijkstra_time = dijkstra_algorithm(G, source_location)


# Display the path with all intermediate locations for Dijkstra's Algorithm
def get_complete_path(source, destination, paths):
    return paths[destination]


# Step 4: Implementing A* Algorithm
def heuristic(a, b, coordinates):
    (lat1, lon1) = coordinates[a]
    (lat2, lon2) = coordinates[b]
    return math.sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2)


# Example coordinates (latitude, longitude) for locations in Hyderabad
coordinates = {
    "Charminar": (17.3616, 78.4747),
    "Secunderabad": (17.4410, 78.4982),
    "HITEC City": (17.4497, 78.3804),
    "Gachibowli": (17.4433, 78.3304),
    "Banjara Hills": (17.4092, 78.4471),
    "Jubilee Hills": (17.4241, 78.4185),
    "Ameerpet": (17.4253, 78.4484),
    "Nampally": (17.3823, 78.4751),
    "Madhapur": (17.4414, 78.3806),
    "LB Nagar": (17.3185, 78.5521),
    "Kondapur": (17.4466, 78.3486),
    "Miyapur": (17.5002, 78.2377),
    "Dilsukhnagar": (17.3690, 78.5611),
    "Saroornagar": (17.3551, 78.5562),
    "Kukatpally": (17.4969, 78.3562),
    "Himayatnagar": (17.4084, 78.4851),
    "Malkajgiri": (17.4522, 78.5661),
    "Medchal": (17.7411, 78.5097),
    "Tarnaka": (17.4352, 78.5239),
    "Borabanda": (17.4502, 78.4295),
    "Nizampet": (17.5076, 78.2892),
    "Chandanagar": (17.4994, 78.2993),
    "Panjagutta": (17.4171, 78.4501),
    "MG Road": (17.4104, 78.4759),
    "Kothapet": (17.3283, 78.5606),
    "Gandhinagar": (17.4189, 78.4757),
    "Begumpet": (17.4391, 78.4483),
    "Balanagar": (17.4873, 78.4384),
    "Malakpet": (17.3787, 78.4939),
    "Nanakramguda": (17.4391, 78.3538),
    "Dundigal": (17.6116, 78.4309),
    "Ramagundam": (17.7237, 78.6542),
    "Saidabad": (17.3595, 78.5467),
    "Shamshabad": (17.2532, 78.3911),
    "Ibrahimpatnam": (17.3361, 78.5028),
    "Bachupally": (17.5257, 78.3734),
    "Necklace Road": (17.4227, 78.4646),
    "KPHB Colony": (17.4834, 78.3871),
    "Mehdipatnam": (17.3958, 78.4312),
    "L B Nagar": (17.3457, 78.5522),
    "Khairatabad": (17.4106, 78.4652),
    "Sainikpuri": (17.4928, 78.5469),
    "Peddamma Temple": (17.4306, 78.4049),
    "Tolichowki": (17.3990, 78.4157),
    "Uppal": (17.3984, 78.5583),
    "LB Stadium": (17.3993, 78.4734),
    "Shilparamam": (17.4526, 78.3783),
    "Shilpakala Vedika": (17.4514, 78.3795),
    "Rajendra Nagar": (17.3220, 78.4023),
    "Ghatkesar": (17.4511, 78.6810),
    "Warasiguda": (17.4165, 78.5135),
    "Hyderabad University": (17.4567, 78.3264),
    "Nizam Institute of Medical Sciences (NIMS)": (17.4219, 78.4520),
    "Osmania University": (17.4180, 78.5273),
    "Ramakrishna Ashram": (17.4117, 78.4815),
    "Mallepally": (17.3893, 78.4589),
    "Koti": (17.3858, 78.4794),
    "Kachiguda": (17.3901, 78.4933),
    "Gachibowli Stadium": (17.4463, 78.3441),
    "Amberpet": (17.3920, 78.5163),
    "Puranapul": (17.3639, 78.4596),
    "AOC Centre": (17.4597, 78.5140),
}

def a_star_algorithm(graph, source, goal, coordinates):
    start_time = time.time()
    path = nx.astar_path(graph, source, goal, weight='weight', heuristic=lambda u, v: heuristic(u, v, coordinates))
    end_time = time.time()
    execution_time = end_time - start_time
    total_cost = sum([graph[u][v]['weight'] for u, v in zip(path[:-1], path[1:])])
    return total_cost, path, execution_time


# Run A* for Charminar to Kukatpally
goal_location = "Kukatpally"
a_star_cost, a_star_path, a_star_time = a_star_algorithm(G, source_location, goal_location, coordinates)


# Step 5: Implementing Floyd-Warshall Algorithm (with Dijkstra)
def floyd_warshall_algorithm(graph):
    start_time = time.time()

    # Use all_pairs_dijkstra_path_length which accepts the 'weight' argument
    all_pairs_shortest_path = dict(nx.all_pairs_dijkstra_path_length(graph, weight='weight'))

    end_time = time.time()
    execution_time = end_time - start_time
    return all_pairs_shortest_path, execution_time


# Run Floyd-Warshall Algorithm (with Dijkstra)
floyd_warshall_paths, floyd_warshall_time = floyd_warshall_algorithm(G)


# Step 6: Implementing BFS & DFS
def bfs_algorithm(graph, source):
    start_time = time.time()
    bfs_path = list(nx.bfs_edges(graph, source))
    end_time = time.time()
    execution_time = end_time - start_time
    return bfs_path, execution_time


def dfs_algorithm(graph, source):
    start_time = time.time()
    dfs_path = list(nx.dfs_edges(graph, source))
    end_time = time.time()
    execution_time = end_time - start_time
    return dfs_path, execution_time


# Run BFS and DFS for Charminar
bfs_path, bfs_time = bfs_algorithm(G, source_location)
dfs_path, dfs_time = dfs_algorithm(G, source_location)

# Output Results
print(f"Dijkstra's Execution Time: {dijkstra_time:.5f} seconds")
print(f"A* Execution Time: {a_star_time:.5f} seconds")
print(f"Floyd-Warshall Execution Time: {floyd_warshall_time:.5f} seconds")
print(f"BFS Execution Time: {bfs_time:.5f} seconds")
print(f"DFS Execution Time: {dfs_time:.5f} seconds")

# Display all paths from Charminar to other locations (intermediate locations included)
print("\nDijkstra's Full Paths from Charminar to All Other Locations:")
for destination in dijkstra_paths:
    print(f"Path to {destination}: {get_complete_path(source_location, destination, dijkstra_paths)}")
