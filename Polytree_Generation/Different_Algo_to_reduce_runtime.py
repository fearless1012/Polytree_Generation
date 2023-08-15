import random

import networkx as nx
import matplotlib.pyplot as plt


def update_connections(G, node, visited, connections):
    visited.add(node)
    component = [node]
    # print(G.neighbors(node))
    for neighbor in G.neighbors(node):
        # print("here")
        # print(G.neighbors(node))
        if neighbor not in visited:
            component.append(update_connections(G, neighbor, visited))

    connections.extend(component)
    # print(connections)
    return connections


def add_edge_to_polytree(G, from_node, to_node):
    # nx.draw(G, with_labels=True, font_weight='bold')
    # plt.show()
    # print(G.nodes[to_node]['connections'])
    # print(G.nodes[from_node]['connections'])

    # Add the edge
    G.add_edge(from_node, to_node)

    # Add all connections of from_node to connections of to_node
    G.nodes[to_node]['connections'] = G.nodes[to_node]['connections'].union(G.nodes[from_node]['connections'])

    # update connections to every other connected node in to_node including the newly added connections of from_node
    for connection in G.nodes[to_node]['connections']:
        G.nodes[connection]['connections'] = G.nodes[connection]['connections'].union(
            G.nodes[to_node]['connections'])

    # # update outputs of from_node
    # G.nodes[from_node]['outputs'].add(to_node)
    # G.nodes[from_node]['outputs'] = G.nodes[from_node]['outputs'].union(G.nodes[to_node]['outputs'])
    # for innode in G.nodes[from_node]['inputs']:
    #     G.nodes[innode]['outputs'] = G.nodes[innode]['outputs'].union(G.nodes[from_node]['outputs'])
    #
    # # update inputs of to_node
    # G.nodes[to_node]['inputs'].add(from_node)
    # G.nodes[to_node]['inputs'] = G.nodes[to_node]['inputs'].union(G.nodes[from_node]['inputs'])
    # for outnode in G.nodes[to_node]['outputs']:
    #     G.nodes[outnode]['inputs'] = G.nodes[outnode]['inputs'].union(G.nodes[to_node]['inputs'])

    # print(G.nodes[to_node]['connections'])
    # print(G.nodes[from_node]['connections'])
    #
    # nx.draw(G, with_labels=True, font_weight='bold')
    # plt.show()


def remove_edge_from_polytree(G, from_node, to_node):
    # nx.draw(G, with_labels=True, font_weight='bold')
    # plt.show()
    # print(G.nodes[to_node]['connections'])
    # print(G.nodes[from_node]['connections'])
    G.remove_edge(from_node, to_node)

    # update connections of every node in from_node
    G_temp = G.to_undirected()
    G.nodes[from_node]['connections'] = nx.node_connected_component(G_temp, from_node)
    G.nodes[to_node]['connections'] = nx.node_connected_component(G_temp, to_node)

    # print(G.nodes[from_node]['connections'])
    # print(G.nodes[to_node]['connections'])

    for connection in G.nodes[to_node]['connections']:
        G.nodes[connection]['connections'] = G.nodes[to_node]['connections']

    for connection in G.nodes[from_node]['connections']:
        G.nodes[connection]['connections'] = G.nodes[from_node]['connections']

    # nx.draw(G, with_labels=True, font_weight='bold')
    # plt.show()


def IsNot_Generalizable(G, intermediary_nodes):
    for i in intermediary_nodes:
        if (G.in_degree(i) == 2 and G.out_degree(i) < 1) or (
                G.in_degree(i) == 1 and G.out_degree(i) < 2) or G.in_degree(i) < 1:
            return False
    return True


def Is_Polytree(G, intermediary_nodes):
    # Fully connected
    if len(G.nodes[1]['connections']) == len(G.nodes()):
        if IsNot_Generalizable(G, intermediary_nodes):
            return True
        else:
            return False
    else:
        return False


def create_polytree_with_e(G, e, possible_edges, intermediary_nodes, graphs, visited):
    # print(e)
    Edges_to_consider = []
    for any_edge in possible_edges:
        if e[0] in any_edge or e[1] in any_edge:
            Edges_to_consider.append(any_edge)

    for edge in Edges_to_consider:
        if edge[0] not in G.nodes[edge[1]]['connections'] and G.in_degree(edge[1]) < 2:
            # print("Adding")
            # print(edge)
            # print(visited)
            visited.append(edge)
            add_edge_to_polytree(G, edge[0], edge[1])
            create_polytree_with_e(G, edge, possible_edges, intermediary_nodes, graphs, visited)
            # print("Removing")
            # print(edge)
            visited.remove(edge)
            remove_edge_from_polytree(G, edge[0], edge[1])

    if Is_Polytree(G, intermediary_nodes) and str(sorted(visited)) not in graphs:
        graphs.append(str(sorted(visited)))
        # print(len(graphs))
        # print(visited)
        # nx.draw(G, with_labels=True, font_weight='bold')
        # plt.show()
        # print(graphs)


def generate_all_polytrees(input_nodes, output_nodes):
    # Max number of output nodes in a polytree would be m+n-2
    max_intermediary_nodes = len(input_nodes) + len(output_nodes) - 1

    for int_node_count in range(max_intermediary_nodes):

        intermediary_nodes = list(range(input_nodes_count + output_nodes_count + 1,
                                        input_nodes_count + output_nodes_count + int_node_count + 1))

        # Create an empty graph
        G = nx.DiGraph()
        G.remove_nodes_from(list(G.nodes()))

        # Add input, output and intermediary nodes to graph
        for node in input_nodes:
            G.add_node(node, label='input', connections=set([node]), connections_dict={})

        for node in output_nodes:
            G.add_node(node, label='output', connections=set([node]), connections_dict={})

        for node in intermediary_nodes:
            G.add_node(node, label='middle', connections=set([node]), connections_dict={})

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

        for m1 in intermediary_nodes:
            for m2 in intermediary_nodes:
                if m1 != m2:
                    possible_edges.append([m1, m2])

        print("Number of intermediary nodes: ", int_node_count)
        print("TotalEdges :", len(possible_edges))
        # print(possible_edges)

        graphs = []
        create_polytree_with_e(G, possible_edges[0], possible_edges, intermediary_nodes, graphs, [])
        print("Number of Graphs Formed : ", len(graphs))
        print("Graphs : ")
        print(graphs)


if __name__ == '__main__':
    # specify number of input nodes and number of output nodes
    input_nodes_count = 3
    output_nodes_count = 2

    input_nodes = list(range(1, input_nodes_count + 1))
    output_nodes = list(range(input_nodes_count + 1, input_nodes_count + output_nodes_count + 1))

    generate_all_polytrees(input_nodes, output_nodes)
