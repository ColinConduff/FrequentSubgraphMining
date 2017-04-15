
import networkx as nx

class Fragment(object):
    
    def __init__(self, source_node_id, current_graph, source_graph, embedding_list):
        self.source_node_id = source_node_id
        self.current_graph = current_graph
        self.source_graph = source_graph
        self.embedding_list = embedding_list

    @property
    def frontier_edges(self):
        for node_id in self.current_graph:
            edges = self.current_graph.edge[node_id]
            for neighbor_id in self.source_graph.neighbors_iter(node_id):
                if neighbor_id not in edges:
                    yield (node_id, neighbor_id)

    def __eq__(self, other):
        pass

    def __hash__(self):
        pass