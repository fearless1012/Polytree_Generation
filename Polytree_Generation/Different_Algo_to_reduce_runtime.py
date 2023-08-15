import random

import networkx as nx
import matplotlib.pyplot as plt


def add_edge_to_polytree(G, from_node, to_node):
    """ ADD THE EDGE TO GRAPH USING BUILT-IN FUNCTION"""
    G.add_edge(from_node, to_node)

    """ UPDATE CONNECTIONS OF TO_NODE/FROM_NODE BY UNIONING THE SET OF CONNECTIONS OF BOTH NODES"""
    G.nodes[to_node]['connections'] = G.nodes[to_node]['connections'].union(G.nodes[from_node]['connections'])

    """ UPDATE CONNECTIONS OF NODES CONNECTED TO TO_NODE/FROM_NODE TO ABOVE UPDATED CONNECTIONS"""
    for connection in G.nodes[to_node]['connections']:
        G.nodes[connection]['connections'] = G.nodes[connection]['connections'].union(
            G.nodes[to_node]['connections'])


def remove_edge_from_polytree(G, from_node, to_node):
    """ REMOVE THE EDGE FROM GRAPH USING BUILT-IN FUNCTION"""
    G.remove_edge(from_node, to_node)

    """ UPDATE CONNECTIONS OF FROM_NODE AND TO_NODE BY CREATING AN UNDIRECTED COPY OF THE GRAPH 
    SO THAT WE CAN USE THE NODE_CONNECTED_COMPONENTS FUNCTION OF NETWORKX"""
    G_temp = G.to_undirected()
    G.nodes[from_node]['connections'] = nx.node_connected_component(G_temp, from_node)
    G.nodes[to_node]['connections'] = nx.node_connected_component(G_temp, to_node)

    """ UPDATE CONNECTIONS OF ALL NODES CONNECTED TO FROM_NODE AND TO_NODE"""
    for connection in G.nodes[to_node]['connections']:
        G.nodes[connection]['connections'] = G.nodes[to_node]['connections']

    for connection in G.nodes[from_node]['connections']:
        G.nodes[connection]['connections'] = G.nodes[from_node]['connections']


def IsNot_Generalizable(G, intermediary_nodes):
    """ GENERALIZABLE CHECKS FOR EVERY INTERMEDIARY NODE
    1. IT HAS AT LEAST ONE INCOMING NODE
    2. IF IT HAS EXACTLY 1 INCOMING NODE, THEN IT HAS AT LEAST 2 OUTGOING NODES
    3. IF IT HAS EXACTLY 2 INCOMING NODE, THEN IT HAS AT LEAST 1 OUTGOING NODE
    NOTE: IT CANNOT HAVE MORE THAN 2 INCOMING NODES AS PER OUR ASSUMPTIONS/CONDITION"""
    for i in intermediary_nodes:
        if (G.in_degree(i) == 2 and G.out_degree(i) < 1) or (
                G.in_degree(i) == 1 and G.out_degree(i) < 2) or G.in_degree(i) < 1:
            return False
    return True


def Is_Polytree(G, intermediary_nodes):
    """ CHECK IF THE TREE IS FULLY CONNECTED, I.E TAKE ANY NODE AND CHECK THAT THE NUMBER OF NODES THAT
    IT IS CONNECTED TO IS EQUAL TO TOTAL NUMBER OF NODES IN THE GRAPH"""
    if len(G.nodes[1]['connections']) == len(G.nodes()):
        """ TO REDUCE RUNTIME, WE CHECK FOR INTERMEDIARY NODES THAT ARE GENERALIZABLE 
        ONLY AFTER ABOVE CONDITION IS SATISFIED"""
        if IsNot_Generalizable(G, intermediary_nodes):
            return True
    return False


def create_polytree_with_e(G, e, possible_edges, intermediary_nodes, graphs, visited):
    """ TAKE ONLY EDGES THAT ARE ADJACENT TO THE CONSIDERED EDGE - TO REDUCE RUNTIME"""
    Edges_to_consider = []
    for any_edge in possible_edges:
        if e[0] in any_edge or e[1] in any_edge:
            Edges_to_consider.append(any_edge)

    """ RECURSIVE CALL TO THE POLYTREE FOR EVERY EDGE IN THE CONSIDERED EDGES"""
    for edge in Edges_to_consider:
        if edge[0] not in G.nodes[edge[1]]['connections'] and G.in_degree(edge[1]) < 2:
            """ VISITED KEEPS A TRACK OF THE GRAPH THAT IS GETTING GENERATED CURRENTLY"""
            visited.append(edge)
            add_edge_to_polytree(G, edge[0], edge[1])
            create_polytree_with_e(G, edge, possible_edges, intermediary_nodes, graphs, visited)
            visited.remove(edge)
            remove_edge_from_polytree(G, edge[0], edge[1])

    """ EVERYTIME THE DFS ALGO REACHES AN END AND EXITS 
    THE FOR LOOP, CHECK IF A NEW POLYTREE HAS BEEN FORMED 
    AND IF SO, ADD IT TO THE LIST OF GRAPHS. I AM CONVERTING THE VISITED
    VARIABLE TO STRING SO THAT THE CHECKING TIME OF IF THE GRAPH IS 
    ALREADY CREATED IS REDUCED """
    if Is_Polytree(G, intermediary_nodes) and str(sorted(visited)) not in graphs:
        graphs.append(str(sorted(visited)))
        nx.draw(G, with_labels=True, font_weight='bold')
        plt.show()


def generate_all_polytrees(input_nodes, output_nodes):
    """ MAXIMUM NUMBER OF INTERMEDIARY NODES WILL BE INPUT+OUTPUT-2 """
    max_intermediary_nodes = len(input_nodes) + len(output_nodes) - 1

    """CREATE AN EMPTY DIRECTED GRAPH"""
    G = nx.DiGraph()

    """ FOR EVERY POSSIBLE INTERMEDIARY NODE COUNT """
    for int_node_count in range(max_intermediary_nodes):

        """ CREATE A LIST OF INTERMEDIARY NODES """
        intermediary_nodes = list(range(input_nodes_count + output_nodes_count + 1,
                                        input_nodes_count + output_nodes_count + int_node_count + 1))

        """ REMOVE ALL NODES FROM THE GRAPH TO CREATE NEW GRAPH """
        G.remove_nodes_from(list(G.nodes()))

        """ ADD THE LIST OF INPUT, OUTPUT AND INTERMEDIARY NODES TO THE GRAPH """
        for node in input_nodes:
            G.add_node(node, label='input', connections=set([node]), connections_dict={})

        for node in output_nodes:
            G.add_node(node, label='output', connections=set([node]), connections_dict={})

        for node in intermediary_nodes:
            G.add_node(node, label='middle', connections=set([node]), connections_dict={})

        """ GET ALL THE POSSIBLE EDGES IN THE GRAPH 
        WHERE INPUT NODES CAN ONLY HAVE OUT-GOING EDGES 
        AND OUTPUT NODES CAN ONLY HAVE INCOMING EDGES """
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
                """CHECK THAT NODES DO NOT FORM SELF-LOOPS"""
                if m1 != m2:
                    possible_edges.append([m1, m2])

        """ EMPTY LIST OF GRAPHS"""
        graphs = []
        """ RECURSIVE FUNCTION TO CREATE POLYTREE WITH DEPTH FIRST SEARCH LIKE ALGORITHM 
        STARTING THE RECURSIVE CALL WITH THE FIRST EDGE IN THE LIST OF POSSIBLE EDGES"""
        create_polytree_with_e(G, possible_edges[0], possible_edges, intermediary_nodes, graphs, [])

        print("Number of intermediary nodes: ", int_node_count)
        print("TotalEdges :", len(possible_edges))
        print("Number of Graphs Formed : ", len(graphs))
        print("Graphs : ")
        print(graphs)
        print("\n")


if __name__ == '__main__':
    """SPECIFY NUMBER OF INPUT NODES AND OUTPUT NODES"""
    input_nodes_count = 3
    output_nodes_count = 3

    """ CREATE THE LISI OF INPUT NODES ADN OUTPUT NODES """
    input_nodes = list(range(1, input_nodes_count + 1))
    output_nodes = list(range(input_nodes_count + 1, input_nodes_count + output_nodes_count + 1))

    """ FUNCTION CALL TO GENERATE ALL POLYTREES"""
    generate_all_polytrees(input_nodes, output_nodes)
