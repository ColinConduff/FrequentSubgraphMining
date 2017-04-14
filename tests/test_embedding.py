
import unittest
import networkx as nx
import source.embedding as emb_module

class EmbeddingTestCase(unittest.TestCase):

    def setUp(self):
        graph = nx.Graph()
        graph.add_node(1, label=0)
        graph.add_node(2, label=0)
        graph.add_edge(1, 2, label=0)
        graph.add_node(3, label=3)
        graph.add_node(4, label=4)
        graph.add_edge(1, 3, label=13)
        graph.add_edge(3, 4, label=34)
        self.small_graph = nx.freeze(graph)

    def test_initial_source_label_is_greater_than_alt_label(self):
        # if source_label > alt_label, should return None
        embedding = emb_module.create_embedding_list_if_unique(self.small_graph, 4, 1)
        self.assertEqual(embedding, None)

    def test_initial_source_label_is_less_than_alt_label(self):
        # if source_label < alt_label, should jump to create_embedding()
        embedding = emb_module.create_embedding_list_if_unique(self.small_graph, 1, 4)
        self.assertEqual(embedding, (0, 0, 0, 13, 3, 34, 4))

    def test_labels_are_identical_and_source_has_smaller_node_ids(self):
        # Use ids to select embedding when labels are identical
        embedding = emb_module.create_embedding_list_if_unique(self.small_graph, 1, 2)
        self.assertEqual(embedding, (0, 0, 0, 13, 3, 34, 4))

    def test_labels_are_identical_and_source_has_larger_node_ids(self):
        # Use ids to select embedding when labels are identical
        embedding = emb_module.create_embedding_list_if_unique(self.small_graph, 2, 1)
        self.assertEqual(embedding, None)
        