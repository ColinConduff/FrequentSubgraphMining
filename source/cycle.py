
from source.fragment import Fragment

class Cycle(Fragment):
    """ A fragment containing a subgraph with one or more cycles. """

    def __init__(self, source_node_id, current_graph, source_graph, embedding_list):
        super().__init__(source_node_id, current_graph, source_graph, embedding_list)

    def __str__(self):
        return "Cycle"

    @property
    def queue_level(self):
        """ A property to specify the search queue containing cycle fragments. """
        from source.search import Level
        return Level.CYCLE