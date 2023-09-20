import numpy as np
import itertools
import networkx as nx
import matplotlib.pyplot as plt
import random

# 生成满足对称性但不满足三角不等式的随机城市距离矩阵
def generate_random_symmetric_distances(num_cities, max_distance=100):
    distances = np.zeros((num_cities, num_cities))
    # 生成随机距离，确保存在对称性
    for i in range(num_cities):
        for j in range(i+1, num_cities):
            distances[i][j] = distances[j][i] = random.randint(1, max_distance)
    
    # 确保不存在城市在一条直线上
    for i in range(num_cities):
        distances[i][(i+1) % num_cities] = random.randint(max_distance + 1, 2 * max_distance)
    
    return distances

# 计算旅行路径的总距离
def calculate_total_distance(tour, distances):
    total_distance = 0
    for i in range(len(tour) - 1):
        total_distance += distances[tour[i]][tour[i + 1]]
    total_distance += distances[tour[-1]][tour[0]]  # 回到起始城市
    return total_distance

# 使用贪心算法寻找最优路径
def find_optimal_tour(distances):
    num_cities = len(distances)
    cities = list(range(num_cities))
    all_permutations = list(itertools.permutations(cities))
    optimal_tour_dict = {}  # 存储每个起点的最优路径和距离

    # 遍历所有城市作为起始城市
    for start_city in cities:
        tour_lengths = []  # 存储每个起点的旅行距离
        for permutation in all_permutations:
            tour = list(permutation)
            tour.insert(0, start_city)  # 在排列的开头插入起始城市
            total_distance = calculate_total_distance(tour, distances)
            tour_lengths.append(total_distance)

        # 如果找到更短的路径，更新最优解
        min_tour_length = min(tour_lengths)
        optimal_tour = list(all_permutations[tour_lengths.index(min_tour_length)])
        optimal_tour.insert(0, start_city)
        optimal_tour_dict[start_city] = {"tour": optimal_tour, "distance": min_tour_length}

    return optimal_tour_dict

# 创建一个有向图表示其中一个最优旅行路径
selected_start_city = 0  # 指定一个起始城市用于可视化
num_cities = 8
distances = generate_random_symmetric_distances(num_cities, max_distance=100)
optimal_tours = find_optimal_tour(distances)
optimal_tour = optimal_tours[selected_start_city]["tour"]
optimal_distance = optimal_tours[selected_start_city]["distance"]
G = nx.DiGraph()

# 添加城市节点
for i, city in enumerate(optimal_tour):
    G.add_node(city, pos=(i, random.randint(-10, 10)))  # 添加一些随机偏移以避免一条直线

# 添加路径边
for i in range(len(optimal_tour)):
    u, v = optimal_tour[i], optimal_tour[(i + 1) % len(optimal_tour)]  # 使用取模确保回到起始城市
    G.add_edge(u, v)

# 绘制有向图
pos = nx.get_node_attributes(G, "pos")
labels = {city: f"{city}" for city in G.nodes}
plt.figure(figsize=(6, 4))
nx.draw(G, pos, with_labels=True, node_size=500, node_color="lightblue", font_size=10)
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): distances[u][v] for u, v in G.edges}, font_size=8)
plt.title(f"Optimal Tour (Total Distance: {optimal_distance})")
plt.show()

# 输出每个起点的最优路径和距离
for start_city, data in optimal_tours.items():
    print(f"Starting from City {start_city}, the optimal tour is {data['tour']} with a total distance of {data['distance']} units.")
