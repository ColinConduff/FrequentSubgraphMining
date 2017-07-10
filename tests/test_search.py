
import unittest
import networkx as nx
from gaston_py import search, factory

class SearchTestCase(unittest.TestCase):

    ORIG_CHEM_DATASET = '../test_files/Chemical_340.txt'
    SMALL_DATASET = '../test_files/small_chemical.txt'

    def setUp(self):
        graph_a = nx.Graph(id=1)
        graph_a.add_node(1, label=0)
        graph_a.add_node(2, label=0)
        graph_a.add_edge(1, 2, label=0)
        self.tiny_graph = nx.freeze(graph_a)

        graph_b = nx.Graph(graph_a)
        graph_b.add_node(3, label=3)
        graph_b.add_edge(1, 3, label=13)
        graph_b.add_edge(2, 3, label=23)
        self.small_graph = nx.freeze(graph_b)
    
    def test_find_frequent_subgraphs_in_tiny_graph(self):

        min_freq = 0
        input_graphs = [self.tiny_graph]

        expected_frequencies = {(0,): 2, (0, 0, 0): 1}

        fragments = factory.initial_node_fragments(input_graphs)
        frequent_output = search.find_frequent_subgraphs(fragments, min_freq)
        frequencies = {embedding: frequent_output[embedding][2] for embedding in frequent_output}

        self.assertEqual(frequencies, expected_frequencies)

    def test_find_frequent_subgraphs_in_small_graph(self):

        min_freq = 0
        input_graphs = [self.small_graph]

        expected_frequencies = {
            (0,): 2,
            (0, 0, 0): 1,
            (0, 0, 0, 13, 3): 1,
            (0, 0, 0, 23, 3): 1,
            # (0, 0, 0, 13, 3, 23, 3): 1,
            (0, 0, 0, 23, 3, 13, 0): 1,
            (0, 13, 3): 1,
            (0, 13, 3, 23, 0): 1,
            (0, 23, 3): 1,
            (3,): 1
        }

        initial_fragments = factory.initial_node_fragments(input_graphs)
        frequent_output = search.find_frequent_subgraphs(initial_fragments, min_freq)
        frequencies = {embedding: frequent_output[embedding][2] for embedding in frequent_output}

        # print(frequencies)

        self.assertEqual(frequencies, expected_frequencies)
