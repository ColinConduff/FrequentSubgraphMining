
from source.fragment import Fragment

class Tree(Fragment):
    def __init__(self, source_node_id, current_graph, source_graph, embedding_list):
        super().__init__(source_node_id, current_graph, source_graph, embedding_list)

    def __str__(self):
        return "Tree"

    @property
    def queue_level(self):
        from source.search import Level
        return Level.TREE
