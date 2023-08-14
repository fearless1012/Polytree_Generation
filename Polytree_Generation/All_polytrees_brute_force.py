import random

import networkx as nx
import matplotlib.pyplot as plt


def generate_all_polytrees(input_nodes, output_nodes):
    # Max number of output nodes in a polytree would be m+n-2
    max_intermediary_nodes = len(input_nodes) + len(output_nodes) - 2

    for int_node_count in range(0, max_intermediary_nodes):
        # Create an empty graph
        G = nx.DiGraph()

        # Add input, output and intermediary nodes to graph
        for node in input_nodes:
            G.add_node(node, label='input', connections=set([node]))

        for node in output_nodes:
            G.add_node(node, label='output', connections=set([node]))

        intermediary_nodes = list(range(input_nodes_count + output_nodes_count + 1,
                                        input_nodes_count + output_nodes_count + int_node_count + 1))

        possible_edges = []
        for i in input_nodes:
            for o in output_nodes:
                possible_edges.append([i, o])

        for i in input_nodes:
            for m in intermediary_nodes:
                possible_edges.append([i, m])

        for m in intermediary_nodes:
            for o in output_nodes:
                possible_edges.append([m, o])

        print(len(possible_edges))
        for e in possible_edges:
            if G.in_degree[e[1]] < 2:
                G.add_edge(e[0], e[1])


    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()


def check_for_generalizablity_of_nodes(G, intermediary_nodes):
    for i in intermediary_nodes:
        if G.in_degree(i) <= 1 and G.out_degree(i) <= 1:
            print("generalized node")


if __name__ == '__main__':
    # specify number of input nodes and number of output nodes
    input_nodes_count = 3
    output_nodes_count = 2

    input_nodes = list(range(1, input_nodes_count + 1))
    output_nodes = list(range(input_nodes_count + 1, input_nodes_count + output_nodes_count + 1))

    generate_all_polytrees(input_nodes, output_nodes)
