
import networkx as nx
from source.fragment import Fragment

class Node(Fragment):
    
    def __init__(self, source_node_id, source_graph):

        node_label = source_graph.node[source_node_id]['label']

        # Move to graph.py
        current_graph = nx.Graph()
        current_graph.add_node(source_node_id, label=node_label)
        current_graph = nx.freeze(current_graph)

        embedding_list = tuple([node_label])

        super().__init__(source_node_id, current_graph, source_graph, embedding_list)

    # def __eq__(self, other):
    #     return self.source_node_id == other.source_node_id

    # def __hash__(self):
    #     return hash(self.source_node_id)

    def __str__(self):
        return "Node"

    @property
    def queue_level(self):
        from source.search import Level
        return Level.NODE
    