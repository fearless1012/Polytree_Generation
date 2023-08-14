import random

import networkx as nx
import matplotlib.pyplot as plt


def add_edge_to_polytree(G, from_node, to_node):
    G.add_edge(from_node, to_node)
    # Add all connections of from_node to connections of to_node
    G.nodes[to_node]['connections'] = G.nodes[to_node]['connections'].union(G.nodes[from_node]['connections'])

    # update connections to every other connected node in to_node
    for connection in G.nodes[to_node]['connections']:
        G.nodes[connection]['connections'] = G.nodes[connection]['connections'].union(
            G.nodes[to_node]['connections'])


def remove_edge_from_polytree(G, from_node, to_node):
    G.remove_edge(from_node, to_node)
    for connection in G.nodes[to_node]['connections']:
        G.nodes[connection]['connections'] = G.nodes[connection]['connections'].difference(
            G.nodes[from_node]['connections'])
    for connection in G.nodes[from_node]['connections']:
        G.nodes[connection]['connections'] = G.nodes[connection]['connections'].difference(
            G.nodes[to_node]['connections'])


def create_polytree_with_e(G, possible_edges, e):
    Edges_to_consider = []
    for any_edge in possible_edges:
        if e[0] in any_edge or e[1] in any_edge:
            Edges_to_consider.append(any_edge)
    Edges_to_consider.remove(e)

    for edge in Edges_to_consider:
        if edge[0] not in G.nodes[edge[1]]['connections'] and G.in_degree(edge[1]) < 2:
            add_edge_to_polytree(G, edge[0], edge[1])
            create_polytree_with_e(G, possible_edges, edge)
        elif len(G.nodes[edge[1]]['connections']) == len(G.nodes()):
            print(len(G.nodes[edge[1]]['connections']), len(G.nodes()))
            nx.draw(G, with_labels=True, font_weight='bold')
            plt.show()


def generate_all_polytrees(input_nodes, output_nodes):
    # Max number of output nodes in a polytree would be m+n-2
    max_intermediary_nodes = len(input_nodes) + len(output_nodes) - 2

    for int_node_count in range(max_intermediary_nodes):

        intermediary_nodes = list(range(input_nodes_count + output_nodes_count + 1,
                                        input_nodes_count + output_nodes_count + int_node_count + 1))

        # Create an empty graph
        G = nx.DiGraph()
        G.remove_nodes_from(list(G.nodes()))

        # Add input, output and intermediary nodes to graph
        for node in input_nodes:
            G.add_node(node, label='input', connections=set([node]))

        for node in output_nodes:
            G.add_node(node, label='output', connections=set([node]))

        for node in intermediary_nodes:
            G.add_node(node, label='middle', connections=set([node]))

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

        for e in possible_edges:
            G.remove_edges_from(list(G.edges()))
            # e is a definite edge in the polytree
            add_edge_to_polytree(G, e[0], e[1])

            create_polytree_with_e(G, possible_edges, e)


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
