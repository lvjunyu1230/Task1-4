import numpy as np
import itertools
import networkx as nx
import matplotlib.pyplot as plt
import random

# Function to generate a random city distance matrix that doesn't satisfy the triangle inequality
def generate_random_distances(num_cities, max_distance=100):
    distances = np.zeros((num_cities, num_cities))
    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            distances[i][j] = random.randint(1, max_distance)
            distances[j][i] = random.randint(1, max_distance)
    return distances

# Function to calculate the total distance of a tour
def calculate_total_distance(tour, distances):
    total_distance = 0
    for i in range(len(tour) - 1):
        total_distance += distances[tour[i]][tour[i + 1]]
    total_distance += distances[tour[-1]][tour[0]]  # Return to the starting city
    return total_distance

# Function to find an optimal tour using the greedy algorithm
def find_optimal_tour_greedy(distances, start_city):
    num_cities = len(distances)
    cities = list(range(num_cities))
    tour = [start_city]
    remaining_cities = cities.copy()
    remaining_cities.remove(start_city)

    while remaining_cities:
        current_city = tour[-1]
        next_city = min(remaining_cities, key=lambda city: distances[current_city][city])
        tour.append(next_city)
        remaining_cities.remove(next_city)

    tour_distance = calculate_total_distance(tour, distances)
    return tour, tour_distance

# Generate a random city distance matrix
num_cities = 8
distances = generate_random_distances(num_cities, max_distance=100)

# Find optimal tours for each starting city using the greedy algorithm
optimal_tours = {}
for start_city in range(num_cities):
    tour, tour_distance = find_optimal_tour_greedy(distances, start_city)
    optimal_tours[start_city] = {"tour": tour, "distance": tour_distance}

# Visualize the optimal tours using NetworkX
G = nx.DiGraph()

# Add city nodes
for i in range(num_cities):
    G.add_node(i, pos=(random.randint(1, 10), random.randint(1, 10)))

# Add tour edges for each starting city
edge_colors = []
for start_city, result in optimal_tours.items():
    tour = result["tour"]
    for i in range(len(tour)):
        u, v = tour[i], tour[(i + 1) % len(tour)]
        G.add_edge(u, v, color=start_city)
        edge_colors.append(start_city)

# Draw the network
pos = nx.get_node_attributes(G, "pos")
edge_colors = [edge_color for _, _, edge_color in G.edges(data="color")]
labels = {city: f"{city}" for city in G.nodes}
plt.figure(figsize=(8, 6))
nx.draw(G, pos, with_labels=True, node_size=500, node_color="lightblue", font_size=10, edge_color=edge_colors, edge_cmap=plt.cm.rainbow)
plt.title("Optimal Tours (Greedy Algorithm)")
plt.show()

# Output the optimal tour data
for start_city, result in optimal_tours.items():
    print(f"Starting from City {start_city}, the optimal tour is {result['tour']} with a total distance of {result['distance']} units.")


