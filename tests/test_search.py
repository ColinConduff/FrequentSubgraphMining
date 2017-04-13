
import unittest
import networkx as nx
import source.search as search
import source.factory as factory

class SearchTestCase(unittest.TestCase):

    ORIG_CHEM_DATASET = '../test_files/Chemical_340.txt'
    SMALL_DATASET = '../test_files/small_chemical.txt'

    def setUp(self):
        graph_a = nx.Graph()
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

        expected_frequencies = {(1,): 1, (2,): 1, (1, 12, 2): 1}

        gaston_objects = factory.initial_nodes(input_graphs)
        frequent_subgraphs, frequencies = search.find_frequent_subgraphs(gaston_objects, min_freq)
        
        self.assertEqual(frequencies, expected_frequencies)