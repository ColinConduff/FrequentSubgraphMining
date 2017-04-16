

class Fragment(object):
    """
    Base class for node, path, tree, and cycle fragments.

    current_graph: a networkx graph representing a subgraph in source_graph
    source_node_id: the id of the source node in the graph
    source_graph: a networkx graph containing current_graph
    embedding_list: a unique tuple representation of current_graph
    """

    def __init__(self, source_node_id, current_graph, source_graph, embedding_list):
        self.source_node_id = source_node_id
        self.current_graph = current_graph
        self.source_graph = source_graph
        self.embedding_list = embedding_list

    @property
    def frontier_edges(self):
        """
        Returns tuples representing edges to neighboring nodes not already in current_graph.
        Used to find possible refinements to fragments.
        """
        for node_id in self.current_graph:
            edges = self.current_graph.edge[node_id]
            if node_id in self.source_graph:
                for neighbor_id in self.source_graph.neighbors_iter(node_id):
                    if neighbor_id not in edges:
                        yield (node_id, neighbor_id)
