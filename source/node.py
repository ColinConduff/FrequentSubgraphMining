
import networkx as nx

class Node(object):
    
    def __init__(self, node_id, source_graph):

        node_label = source_graph.node[node_id]['label']

        self.current_graph = nx.Graph()
        self.current_graph.add_node(node_id, label=node_label)
        self.current_graph = nx.freeze(self.current_graph)

        # self.frontier_edges = frozenset(
        #     (node_id, neighbor_id) for neighbor_id in source_graph.neighbors_iter(node_id))

        self.embedding_list = tuple([node_label])

        self.node_id = node_id
        self.source_graph = source_graph
    
    def __iter__(self):
        return iter((self.node_id, self.frontier_edges, self.source_graph))

    @property
    def frontier_edges(self):
        neighbors = self.source_graph.neighbors_iter(self.node_id)
        return ((self.node_id, neighbor_id) for neighbor_id in neighbors)

    def __eq__(self, other):
        return self.node_id == other.node_id

    def __hash__(self):
        return hash(self.node_id)