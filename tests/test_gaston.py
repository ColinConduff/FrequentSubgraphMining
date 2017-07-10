
import unittest
import networkx as nx
from gaston_py.gaston import gaston

class GastonTestCase(unittest.TestCase):

    ORIG_CHEM_DATASET = 'test_files/Chemical_340.txt'
    SMALL_DATASET = 'test_files/small_chemical.txt'
    MEDIUM_DATASET = 'test_files/medium_chemical.txt'

    def test_gaston_with_small_dataset(self):

        frequent_output = gaston(min_support=6,
                                 input_file=GastonTestCase.SMALL_DATASET)

        self.assertTrue(all(isinstance(key, tuple) for key in frequent_output.keys()))
        self.assertTrue(all(isinstance(value, tuple) for value in frequent_output.values()))

        allowed_graph_types = set(['Node', 'Path', 'Tree', 'Cycle'])
        for nx_graph, graph_type, frequency in frequent_output.values():
            self.assertTrue(isinstance(nx_graph, nx.Graph))
            self.assertTrue(graph_type in allowed_graph_types)
            self.assertTrue(isinstance(frequency, int))
            self.assertTrue(frequency >= 0)

    def test_does_not_generate_unwanted_graph_types(self):
        frequent_output = gaston(min_support=0.95,
                                 input_file=GastonTestCase.SMALL_DATASET,
                                 dont_generate_trees=True,
                                 dont_generate_cycles=True)

        unwanted_graph_types = set(['Tree', 'Cycle'])
        for _, graph_type, _ in frequent_output.values():
            self.assertTrue(graph_type not in unwanted_graph_types)
