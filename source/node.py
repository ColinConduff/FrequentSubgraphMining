
import networkx as nx
from source.fragment import Fragment

class Node(Fragment):
    
    def __init__(self, source_node_id, source_graph):

        node_label = source_graph.node[source_node_id]['label']

        current_graph = nx.Graph()
        current_graph.add_node(source_node_id, label=node_label)
        current_graph = nx.freeze(current_graph)

        embedding_list = tuple([node_label])

        super().__init__(source_node_id, current_graph, source_graph, embedding_list)
    
    def __iter__(self):
        return iter((self.source_node_id, self.frontier_edges, self.source_graph))

    def __eq__(self, other):
        return self.source_node_id == other.source_node_id

    def __hash__(self):
        return hash(self.source_node_id)