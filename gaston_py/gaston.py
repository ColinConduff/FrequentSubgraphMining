
from collections import Counter

import gaston_py.graph as graph_module
import gaston_py.factory as factory
import gaston_py.search as search

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

    print("Frequent Subgraphs:")
    for embedding_list, (_, _, frequency) in frequent_output.items():
        print("embedding_list: {}, frequency: {}".format(''.join(embedding_list), frequency))
