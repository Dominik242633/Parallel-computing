import networkx as nx
import matplotlib.pyplot as plt

verticies_number = 5
# graph = [[0, 2, 0, 6],
#          [2, 0, 3, 8],
#          [0, 3, 0, 0],
#          [6, 8, 0, 0]]

graph = [[0, 2, 0, 6, 0],
         [2, 0, 3, 8, 5],
         [0, 3, 0, 0, 7],
         [6, 8, 0, 0, 9],
         [0, 5, 7, 9, 0]]


def print_tree(parent):
    print("Edge \tWeight")

    for i in range(1, verticies_number):
        print(parent[i], "-", i, "\t", graph[i][parent[i]])


def plot_tree(parent):
    G = nx.Graph()

    for i in range(len(parent)):
        G.add_node(i)

    for i in range(1, len(parent)):
        G.add_edge(parent[i], i, weight=graph[i][parent[i]])

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)

    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    plt.show()


def min_vertex(key, vertex_is_included):
    minimum = 10000

    for v in range(verticies_number):
        if key[v] < minimum and not vertex_is_included[v]:
            minimum = key[v]
            min_index = v

    return min_index


key = [10000 for _ in range(verticies_number)]

parent = [None for _ in range(verticies_number)]

key[0] = 0
vertex_is_included = [False for i in range(verticies_number)]

parent[0] = -1

for cout in range(verticies_number):
    u = min_vertex(key, vertex_is_included)

    vertex_is_included[u] = True

    for v in range(verticies_number):
        if graph[u][v] > 0 and not vertex_is_included[v] and key[v] > graph[u][v]:
            key[v] = graph[u][v]
            parent[v] = u

print_tree(parent)
plot_tree(parent)