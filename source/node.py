
import networkx as nx
from source.factory import Embedding

class Node(object):
    
    def __init__(self, node_id, source_graph):

        node_label = source_graph.node[node_id]['label']

        self.current_graph = nx.Graph()
        self.current_graph.add_node(node_id, label=node_label)
        self.current_graph = nx.freeze(self.current_graph)

        self.frontier_edges = frozenset((node_id, neighbor_id) for neighbor_id in source_graph.neighbors(node_id))

        self.embedding_list = Embedding(ids=tuple([node_id]), labels=tuple([node_label]))

        self.node_id = node_id
        self.source_graph = source_graph
    
    def __iter__(self):
        return iter((self.node_id, self.frontier_edges, self.source_graph))