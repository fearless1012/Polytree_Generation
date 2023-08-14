import random

import networkx as nx
import matplotlib.pyplot as plt


def create_initial_tree(G, input_nodes, output_nodes):
    # Max number of output nodes in a polytree would be m+n-2
    max_intermediary_nodes = input_nodes_count + output_nodes_count - 2

    # Randomize number of intermediary nodes
    intermediary_nodes_count = random.randint(0, max_intermediary_nodes)
    intermediary_nodes = list(range(input_nodes_count + output_nodes_count + 1,
                                    input_nodes_count + output_nodes_count + max_intermediary_nodes + 1))

    # Add input, output and intermediary nodes to graph
    for node in input_nodes:
        G.add_node(node, label='input', connections=set([node]))

    for node in output_nodes:
        G.add_node(node, label='output', connections=set([node]))

    for node in intermediary_nodes:
        G.add_node(node, label='middle', connections=set([node]))

    nodes_with_incoming_edges = output_nodes + intermediary_nodes
    nodes_with_outgoing_edges = input_nodes + intermediary_nodes
    components = list(nx.weakly_connected_components(G))

    total_number_of_nodes = len(input_nodes) + len(output_nodes) + len(intermediary_nodes)

    while len(G.nodes[1]['connections']) < total_number_of_nodes and len(nodes_with_incoming_edges) > 0:
        from_node = random.choice(nodes_with_outgoing_edges)
        to_node = random.choice(nodes_with_incoming_edges)

        if from_node not in G.nodes[to_node]['connections']:
            edge = [from_node, to_node]
            print(edge)
            G.add_edge(edge[0],edge[1])
            G.nodes[to_node]['connections'] = G.nodes[to_node]['connections'].union(G.nodes[from_node]['connections'])

            print(G.nodes[to_node])

            for connection in G.nodes[to_node]['connections']:
                G.nodes[connection]['connections'] = G.nodes[connection]['connections'].union(
                    G.nodes[to_node]['connections'])

            if G.in_degree[to_node] >= 2:
                nodes_with_incoming_edges.remove(to_node)

            # connect all disjoint components
            components = list(nx.weakly_connected_components(G))

    return G


def check_for_generalizablity_of_nodes(G, intermediary_nodes):
    for i in intermediary_nodes:
        if G.in_degree(i) <= 1 and G.out_degree(i) <= 1:
            print("generalized node")


def generate_random_polytrees(input_nodes, output_nodes, polytree_count):
    # Create an empty graph
    G = nx.DiGraph()

    G = create_initial_tree(G, input_nodes, output_nodes)
    print(G.nodes.data())

    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()


if __name__ == '__main__':
    # specify number of input nodes and number of output nodes
    input_nodes_count = 3
    output_nodes_count = 2

    input_nodes = list(range(1, input_nodes_count + 1))
    output_nodes = list(range(input_nodes_count + 1, input_nodes_count + output_nodes_count + 1))

    number_of_sample_polytrees = 10
    generate_random_polytrees(input_nodes, output_nodes, number_of_sample_polytrees)
