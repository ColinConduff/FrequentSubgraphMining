class Tree(object):
    def __init__(self, root_node_id, current_graph, 
                     frontier_edges, source_graph, embedding_list):
        self.root_node_id, self.current_graph = root_node_id, current_graph
        self.frontier_edges, self.source_graph = frontier_edges, source_graph
        self.embedding_list = embedding_list
