
import unittest
import networkx as nx
import source.factory as factory
from source.node import Node
from source.path import Path
from source.tree import Tree
from source.cycle import Cycle

class FactoryTestCase(unittest.TestCase):

    def setUp(self):
        graph = nx.Graph(id=1)
        graph.add_node(1, label=0)
        graph.add_node(2, label=0)
        graph.add_edge(1, 2, label=0)
        graph.add_node(3, label=3)
        graph.add_node(4, label=4)
        graph.add_edge(1, 3, label=13)
        graph.add_edge(3, 4, label=34)
        self.small_graph = nx.freeze(graph)

    def test_initial_node_fragments(self):
        node_fragments = factory.initial_node_fragments([self.small_graph])
        self.assertTrue(all(isinstance(x, Node) for x in node_fragments))

    def test_apply_refinement_func_creates_paths_from_nodes(self):
        prev_fragment = Node(1, self.small_graph)
        edge = (1, 2)
        fragment = factory.apply_refinement(prev_fragment, edge,
                                            dont_generate_cycles=False, dont_generate_trees=False)
        self.assertTrue(isinstance(fragment, Path))
        