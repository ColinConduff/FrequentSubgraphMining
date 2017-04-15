
"""
Gaston finds all frequent subgraphs by using a level-wise approach in which first simple paths are considered, 
then more complex trees and finally the most complex cyclic graphs. It appears that in practice most frequent 
graphs are not actually very complex structures; Gaston uses this quickstart observation to organize the search 
space efficiently. To determine the frequency of graphs, Gaston employs an occurrence list based approach in 
which all occurrences of a small set of graphs are stored in main memory.

Parsemis approach:

Parse input into graphs
Mine fragments from the graphs

Create database
    - Compute frequency of nodes and labels
    - Sort by frequency
    - Remove infrequent nodes and labels

Create GastonGraph for each input graph
    For each node
        if node_label does not already have a path
        Create subgraph
        Add node to subgraph
        Create Refinement
        Create Fragment
        Create Leg 
        Create Path

"""
import functools
import networkx as nx
import matplotlib.pyplot as plt

import source.factory as factory
import source.search as search

ORIG_CHEM_DATASET = 'test_files/Chemical_340.txt'
SMALL_DATASET = 'test_files/small_chemical.txt'

OUTPUT_FILEPATH = "output_files/output.txt"

def gaston():
    min_freq = 10
    graphs = read_line_graphs(SMALL_DATASET)

    print("Graph count: {}, total nodes: {}, total edges: {}".format(
        len(graphs), count_total_nodes(graphs), count_total_edges(graphs)))
    print("Unique nodes: {}, unique edges: {}".format(
        count_unique_nodes(graphs), count_unique_edges(graphs)))

    # for graph in graphs:
    #     nx.draw_networkx(graph)
    #     # nx.draw_networkx_labels(graph)
    #     plt.show()

    fragments = factory.initial_nodes(graphs)
    frequent_subgraphs, frequencies = search.find_frequent_subgraphs(fragments, min_freq)

    for embedding_list, subgraph in frequent_subgraphs.items():
        frequency = frequencies[embedding_list]
        print("embedding_list: {}, frequency: {}".format(''.join(embedding_list), frequency))

        nx.write_gml(subgraph, OUTPUT_FILEPATH)

def read_line_graphs(file_path):
    """
    Returns a list of NetworkX graph objects read from a line graph file.
    """
    graph_map = {}

    with open(file_path, "r") as f:
        graph_id = 0

        for line in f:
            line = line.strip()
            characters = line.split(" ")

            if line.startswith("t #"):
                graph_id += 1
                graph = nx.Graph(id=graph_id, embeddings=[])
                graph_map[graph_id] = graph

            elif line.startswith("v"):
                label = " ".join(characters[2:]).strip('\'')
                graph_map[graph_id].add_node(characters[1], label=label)

            elif line.startswith("e"):
                label = " ".join(characters[3:]).strip('\'')
                graph_map[graph_id].add_edge(characters[1], characters[2], label=label)

            elif line.startswith("#=>"):
                embedding = characters[1]
                graph_map[graph_id].graph['embeddings'].append(embedding)

    # Return frozen graphs
    return [nx.freeze(graph) for graph in graph_map.values()]

def count_total_nodes(graphs):
    return functools.reduce(lambda total, graph: total + graph.number_of_nodes(), graphs, 0)

def count_total_edges(graphs):
    return functools.reduce(lambda total, graph: total + graph.number_of_edges(), graphs, 0)

def count_unique_nodes(graphs):
    return len(set(data['label'] for graph in graphs for _,data in graph.nodes_iter(data=True)))

def count_unique_edges(graphs):
    return len(set(edge['label'] for graph in graphs for _,_,edge in graph.edges_iter(data=True)))

# def find_paths(gaston_subgraph):
#     for frontier_edge in gaston_subgraph.frontier_edges:
#         # if is_valid_refinement():
#         apply_refinement(gaston_subgraph, frontier_edge)

#     for leg in legs:
#         refined_subgraph = apply_refinement_to_path(l.refinement, path)
#         joined_legs = set(join(leg, other_leg) for other_leg in legs if leg != other_leg)
#         if l.refinement.is_cycle_refinement:
#             # next_legs = next_legs??? + joined_legs
#             find_cyclic_graphs(refined_subgraph, next_legs)
#         else:
#             next_legs = extend(leg) + joined_legs
#             if refined_subgraph.graph_type = GraphType.PATH:
#                 find_paths(refined_subgraph, next_legs)
#             else:
#                 find_trees(refined_subgraph, next_legs)

# def find_trees(tree, legs):
#     for leg in legs:
#         refined_subgraph = apply_refinement_to_tree(l.refinement, tree)
#         joined_legs = set(join(leg, other_leg) for other_leg in legs if leg != other_leg)
#         if l.refinement.is_cycle_refinement:
#             # next_legs = next_legs??? + joined_legs
#             find_cyclic_graphs(refined_subgraph, next_legs)
#         else:
#             next_legs = restricted_extend(leg) + joined_legs
#             find_trees(refined_subgraph, next_legs)

# def find_cyclic_graphs(graph, legs):
#     for leg in legs:
#         refined_subgraph = apply_refinement_to_graph(l.refinement, graph)
#         joined_legs = set(join(leg, other_leg) for other_leg in legs if other_leg > leg)
#         # next_legs = next_legs??? + joined_legs
#         find_cyclic_graphs(refined_subgraph, next_legs)

# def join(leg1, leg2):
#     new_leg.refinement = leg2.refinement
#     new_leg.embedding_list = []
#     for k, tk in enumerate(leg1.embedding_list):
#         for tj in leg2.embedding_list:
#             if tk.parent == tj.parent:
#                 new_leg.embedding_list.append(k, tj.graph, tj.node)

#     if new_leg is freqent:
#         return new_leg
#     else:
#         return None

# def extend(leg):
#     candidate_legs = []
#     for k, tk in enumerate(leg.embedding_list):
#         for neighbor in tk.neighbors:
#             if neighbor in tk.embedding_list:
#                 # leg creates cycle
#                 # candidate_leg.embedding_list.append(k, ???, ???)
#             else:
#                 # node refinement leg
#                 candidate_leg.embedding_list.append(k, neighbor, t.graph)
#     return [candidate for candidate in candidate_legs if candidate is frequent]
