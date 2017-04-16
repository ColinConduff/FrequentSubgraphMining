"""
"Gaston finds all frequent subgraphs by using a level-wise approach in which first simple paths are considered, 
then more complex trees and finally the most complex cyclic graphs. It appears that in practice most frequent 
graphs are not actually very complex structures; Gaston uses this quickstart observation to organize the search 
space efficiently. To determine the frequency of graphs, Gaston employs an occurrence list based approach in 
which all occurrences of a small set of graphs are stored in main memory." - Siegfried Nijssen (Gaston author)
"""
import sys, getopt
from collections import Counter

import source.graph as graph_module
import source.factory as factory
import source.search as search

HELP_TEXT = 'main.py -s <min support> -i <inputfile> -o <outputfile> -c <no cycles> -t <no trees>'

def command_line_interface(argv):
    """
    A command line interface for interacting with the gaston python implementation.
    Args:
        min_support: a float or integer
        input_file: file path to a text file in line graph format
        output_file: file path to output frequent subgraphs in line graph format
        dont_generate_cycles: a flag to specify that cycles should not be generated
        don_generate_trees: a flag to specify that trees should not be generated
    """

    min_support = None
    input_file = None
    output_file = None
    dont_generate_cycles = False
    dont_generate_trees = False

    try:
        opts, _ = getopt.getopt(argv, "hs:m:i:o:ct")
    except getopt.GetoptError:
        print(HELP_TEXT)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(HELP_TEXT)
            sys.exit()
        elif opt == "-s":
            min_support = float(arg)
        elif opt == "-i":
            input_file = arg
        elif opt == "-o":
            output_file = arg
        elif opt == "-c":
            dont_generate_cycles = True
        elif opt == "-t":
            dont_generate_trees = True

    if input_file is None or min_support is None:
        print("Input file and minimum support must be specified.")
        print(HELP_TEXT)
        sys.exit(2)
    elif min_support <= 0:
        print("Minimum support must be greater than 0.")
        sys.exit(2)

    print("\nMinimum Support:{}".format(min_support))
    
    if dont_generate_cycles:
        print("Cycles will not be generated.")

    if dont_generate_trees:
        print("Trees will not be generated.")

    frequent_output = gaston(min_support, input_file,
                             dont_generate_cycles, dont_generate_trees,
                             should_print_graph_information=True)

    if output_file is not None:
        write_frequent_subgraphs_to_file_path(output_file, frequent_output)

    print_statistics(frequent_output)

def gaston(min_support, input_file,
           dont_generate_cycles=False, dont_generate_trees=False,
           should_print_graph_information=False):
    """
    Reads graphs from a line graph file and finds frequently occurring
    subgraphs with support > min_support.

    Args:
        min_support: a float specifying the minimum support
        input_file: a file path to the input file containing line graphs
        dont_generate_cycles: a flag specifying whether to generate cycles
        dont_generate_trees: a flag specifying whether to generate trees
        should_print_graph_information: a flag specifying whether to print graph info

    Returns:
        a dictionary of the form {embedding_list: (subgraph, graph type, frequency)}
    """

    graphs = graph_module.read_line_graphs(input_file)
    min_frequency = int(min_support * len(graphs))
    if min_frequency < 1:
        min_frequency = 1

    if should_print_graph_information:
        print_graph_information(graphs, min_frequency)

    fragments = factory.initial_node_fragments(graphs)
    return search.find_frequent_subgraphs(fragments, min_frequency,
                                          dont_generate_cycles, dont_generate_trees)

def print_graph_information(graphs, min_frequency):
    """ Prints relevant graph information such as min frequency and counts. """
    print("\nMinimum Frequency: {}".format(min_frequency))
    print("Total - graphs: {}, nodes: {}, edges: {}".format(
        len(graphs),
        graph_module.count_total_nodes(graphs),
        graph_module.count_total_edges(graphs)))

    print("Unique - nodes: {}, edges: {}\n".format(
        graph_module.count_unique_nodes(graphs), graph_module.count_unique_edges(graphs)))

def write_frequent_subgraphs_to_file_path(output_file, frequent_output):
    """ Writes frequently occurring subgraphs to the output filepath. """
    frequent_graph_iter = iter(graph for graph, _, _ in frequent_output.values())
    graph_module.write_line_graphs(frequent_graph_iter, output_file)

def print_statistics(frequent_output):
    """ Prints frequencies by graph type and embedding list. """
    graph_type_frequency = Counter(graph_type for _, graph_type, _ in frequent_output.values())

    print("Frequencies:")
    print("Nodes: {}".format(graph_type_frequency['Node']))
    print("Paths: {}".format(graph_type_frequency['Path']))
    print("Trees: {}".format(graph_type_frequency['Tree']))
    print("Cycles: {}\n".format(graph_type_frequency['Cycle']))
    
    for embedding_list, (_, _, frequency) in frequent_output.items():
        print("embedding_list: {}, frequency: {}".format(''.join(embedding_list), frequency))

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
