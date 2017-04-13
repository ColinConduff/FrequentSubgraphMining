class Cycle(object):
    def __init__(self, source_node_id, current_graph, 
                     frontier_edges, source_graph, embedding_list):
        self.source_node_id, self.current_graph = source_node_id, current_graph
        self.frontier_edges, self.source_graph = frontier_edges, source_graph
        self.embedding_list = embedding_list
