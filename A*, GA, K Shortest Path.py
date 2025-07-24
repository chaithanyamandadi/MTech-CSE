import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
import time
from itertools import islice

# Define the graph with locations and distances
locations = {
    "Uppal": (0, 0),
    "Secunderabad": (2, 3),
    "Ameerpet": (5, 1),
    "Madhapur": (7, 4),
    "Gachibowli": (8, 2),
    "Dilsukhnagar": (3, 5),
    "Mehdipatnam": (6, 3),
    "Hitech City": (9, 6),
    "Begumpet": (4, 7),
    "Kukatpally": (10, 5)
}

# Define edges with distances in km
edges = {
    ("Uppal", "Secunderabad"): 10.2,
    ("Secunderabad", "Ameerpet"): 5.8,
    ("Ameerpet", "Madhapur"): 6.5,
    ("Madhapur", "Gachibowli"): 4.7,
    ("Gachibowli", "Kukatpally"): 8.0,
    ("Uppal", "Dilsukhnagar"): 7.3,
    ("Dilsukhnagar", "Mehdipatnam"): 9.1,
    ("Mehdipatnam", "Hitech City"): 5.5,
    ("Hitech City", "Begumpet"): 7.2,
    ("Begumpet", "Kukatpally"): 6.9,
    ("Ameerpet", "Begumpet"): 3.6,
    ("Dilsukhnagar", "Secunderabad"): 8.3,
    ("Mehdipatnam", "Madhapur"): 4.2,
    ("Begumpet", "Secunderabad"): 5.0,
    ("Begumpet", "Ameerpet"): 4.0
}

# Create a graph
G = nx.Graph()

# Add nodes
for node, pos in locations.items():
    G.add_node(node, pos=pos)

# Add edges with weights
for edge, distance in edges.items():
    G.add_edge(edge[0], edge[1], weight=distance)


# A* Algorithm Implementation
def a_star_search(graph, start, goal):
    return nx.astar_path(graph, start, goal, weight="weight")


# Ensure GA only generates valid routes
def create_valid_route(graph, nodes):
    while True:
        route = random.sample(nodes, len(nodes))
        if all(graph.has_edge(route[i], route[i+1]) for i in range(len(route) - 1)):
            return route  # Ensures that the route is fully connected

# Fitness function with validity check
def fitness(route, graph):
    total_distance = 0
    for i in range(len(route) - 1):
        if graph.has_edge(route[i], route[i + 1]):
            total_distance += graph[route[i]][route[i + 1]]['weight']
        else:
            return float('inf')  # Penalize invalid routes
    return 1 / (total_distance + 1e-6)


# Crossover ensuring valid routes
def crossover(parent1, parent2, graph):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [None] * size
    child[start:end] = parent1[start:end]

    remaining = [node for node in parent2 if node not in child]
    pointer = 0
    for i in range(size):
        if child[i] is None:
            child[i] = remaining[pointer]
            pointer += 1

    return child if all(graph.has_edge(child[i], child[i+1]) for i in range(len(child)-1)) else parent1

# Mutation ensuring valid routes
def mutate(route, graph):
    i, j = sorted(random.sample(range(len(route)), 2))
    if graph.has_edge(route[i], route[j]):  # Swap only if edge exists
        route[i], route[j] = route[j], route[i]
    return route

# Genetic Algorithm with Elitism
def genetic_algorithm(graph, nodes, population_size=100, generations=500):
    population = [create_valid_route(graph, nodes) for _ in range(population_size)]

    for gen in range(generations):
        population.sort(key=lambda x: fitness(x, graph), reverse=True)

        # Keep track of best valid solutions
        best_fitness = fitness(population[0], graph)
        print(f"Generation {gen}: Best Fitness Score = {best_fitness}")

        # If GA starts producing invalid solutions, stop early
        if best_fitness == float('inf'):
            print("GA is losing valid solutions! Adjusting...")
            break

            # Elitism: Keep the top 10 valid routes
        next_gen = population[:10]
        for _ in range(population_size - 10):
            parent1, parent2 = random.sample(population[:50], 2)
            child = parent1[:len(parent1) // 2] + parent2[len(parent2) // 2:]
            if random.random() < 0.1:
                random.shuffle(child)  # Mutation by shuffling nodes
            next_gen.append(child)

        population = next_gen

    return population[0], fitness(population[0], graph)

# Hybrid Algorithm: A* + GA
def hybrid_algorithm(graph, start, goal, nodes, population_size=100, generations=500):
    initial_path = a_star_search(graph, start, goal)[1:-1]
    best_route, best_fitness = genetic_algorithm(graph, initial_path, population_size, generations)
    return [start] + best_route + [goal], best_fitness

def compute_route_distance(graph, route):
    if all(graph.has_edge(route[i], route[i+1]) for i in range(len(route) - 1)):
        return sum(graph[route[i]][route[i+1]]['weight'] for i in range(len(route) - 1))
    else:
        return float('inf')  # Assign a high penalty instead of crashing

# Compute execution times
start_time = time.time()
a_star_path = a_star_search(G, "Uppal", "Kukatpally")
a_star_time = time.time() - start_time

start_time = time.time()
ga_route, ga_fitness = genetic_algorithm(G, list(G.nodes)[1:-1])
ga_time = time.time() - start_time

start_time = time.time()
hybrid_route, hybrid_fitness = hybrid_algorithm(G, "Uppal", "Kukatpally", list(G.nodes)[1:-1])
hybrid_time = time.time() - start_time

# Compute K Shortest Paths execution time
start_time = time.time()
k = 5  # Number of shortest paths to retrieve
shortest_routes = list(islice(nx.shortest_simple_paths(G, source="Uppal", target="Kukatpally", weight="weight"), k))
shortest_time = time.time() - start_time

# Compute total distance for each route
shortest_routes_with_distance = []
for route in shortest_routes:
    total_distance = sum(G[route[i]][route[i+1]]['weight'] for i in range(len(route)-1))
    shortest_routes_with_distance.append((route, total_distance))

# Determine the best path based on distance
best_path = min(shortest_routes_with_distance, key=lambda x: x[1])

# Display all paths and the best path
print(f"\nAll {k} Shortest Routes Found:")
for i, (route, distance) in enumerate(shortest_routes_with_distance, start=1):
    print(f"Route {i} (Distance: {distance:.2f} km): {route}")

print(f"\nBest Path Based on Distance: {best_path[0]} (Distance: {best_path[1]:.2f} km)")

# Determine the best algorithm
execution_times = {
    "A* Algorithm": (a_star_time, compute_route_distance(G, a_star_path)),
    "Genetic Algorithm": (ga_time, compute_route_distance(G, ga_route) if ga_route else float('inf')),
    "Hybrid Algorithm": (hybrid_time, compute_route_distance(G, hybrid_route) if hybrid_route else float('inf')),
    "K Shortest Paths": (shortest_time, best_path[1])
}

best_algorithm = min(execution_times, key=lambda x: execution_times[x][1])

# Display results
print(f"\nA* Optimized Path: {a_star_path}")
print(f"Genetic Algorithm Optimized Route: {['Uppal'] + ga_route + ['Kukatpally']}")
print(f"Hybrid Algorithm Optimized Route: {hybrid_route}")

print(f"\nBest Performing Algorithm: {best_algorithm}")
for algo, (time_taken, distance) in execution_times.items():
    print(f"{algo}: Execution Time = {time_taken:.6f} sec, Distance = {distance:.2f} km")

# Visualize the Graph
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", edge_color="gray", font_size=10)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f"{d['weight']:.2f} km" for u, v, d in G.edges(data=True)})
plt.title("Hyderabad Road Network (10 Places)")
plt.show()