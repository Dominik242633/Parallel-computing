import networkx as nx
import matplotlib.pyplot as plt
from mpi4py import MPI

comm = MPI.COMM_WORLD
my_rank = comm.Get_rank()
p = comm.Get_size()

vertices_number = 6
vertices_per_processor = int(vertices_number / p)

# graph = [[0, 2, 0, 6],
#          [2, 0, 3, 8],
#          [0, 3, 0, 0],
#          [6, 8, 0, 0]]

graph = [[0, 2, 0, 6, 0, 3],
         [2, 0, 3, 8, 5, 2],
         [0, 3, 0, 0, 7, 0],
         [6, 8, 0, 0, 9, 1],
         [0, 5, 7, 9, 0, 1],
         [1, 2, 0, 3, 4, 0]]

# graph = [[0, 2, 0, 6, 0],
#          [2, 0, 3, 8, 5],
#          [0, 3, 0, 0, 7],
#          [6, 8, 0, 0, 9],
#          [0, 5, 7, 9, 0]]


def print_tree(parent):
    print("Edge \tWeight")

    for i in range(1, vertices_number):
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
    min_index = 0
    print(f"Processor: {my_rank}, key: {key}, vertex_is_included: {vertex_is_included}")
    for v in range(len(vertex_is_included)):
        if key[v] < minimum and not vertex_is_included[v]:
            minimum = key[v]
            min_index = v

    return min_index


if my_rank == 0:
    # Minimum weight edge
    key = [10000 for _ in range(vertices_number)]

    # List with parent vertices - e.g. parent[5] = 3 -> vertex 5 has connection with vertex 3
    parent = [None for _ in range(vertices_number)]
    parent[0] = -1  # start from vertex 0
    key[0] = 0

    # Is vertex included - True or False
    vertex_is_included = [False for i in range(vertices_number)]

    # Main loop for all vertices
    for _ in range(vertices_number):
        if p != 1:
            local_key = key[:vertices_per_processor]
            local_vertex_is_included = vertex_is_included[:vertices_per_processor]
        else:
            local_key = key[:]
            local_vertex_is_included = vertex_is_included[:]

        # Send and receive data from other processors
        for processor_number in range(1, p):
            start_number = vertices_per_processor * processor_number
            end_number = vertices_per_processor * (processor_number+1)
            if processor_number != p:
                comm.send([key[start_number: end_number],
                           vertex_is_included[start_number: end_number]], dest=processor_number)
            else:
                comm.send([key[start_number:],
                           vertex_is_included[start_number:]], dest=processor_number)

        # Create list with local closest vertices
        local_solutions = [min_vertex(local_key, local_vertex_is_included)]
        for processor_number in range(1, p):
            local_solutions.append(comm.recv(source=processor_number))

        # print(f"local_solutions: {local_solutions}")
        u = local_solutions[0]
        local_weight = key[u]
        # Find global solution
        for solution in local_solutions:
            if key[solution] < local_weight:
                local_weight = key[solution]
                u = solution
        # print(f"u: {u}")
        # Include it in list
        vertex_is_included[u] = True

        # Update key and parent lists
        for v in range(vertices_number):
            # If edge is greater than 0 (exists) and current distance is greater than new distance
            # and vertex is not included
            if key[v] > graph[u][v] > 0 and not vertex_is_included[v]:
                # print(f"Key: {key}")
                key[v] = graph[u][v]
                parent[v] = u

    print_tree(parent)

else:
    for _ in range(vertices_number):
        # Receive data
        local_key, local_vertex_is_included = comm.recv(source=0)
        local_key[0] = 9999
        print(f"local_key: {local_key}, local_vertex_is_included: {local_vertex_is_included}")

        # Find local closest vertex
        u = min_vertex(local_key, local_vertex_is_included)

        comm.send(u, dest=0)

MPI.Finalize()
