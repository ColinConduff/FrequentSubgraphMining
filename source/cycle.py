
from source.fragment import Fragment
from source.level import Level

class Cycle(Fragment):
    """ A fragment containing a subgraph with one or more cycles. """

    def __str__(self):
        return "Cycle"

    @property
    def queue_level(self):
        """ A property to specify the search queue containing cycle fragments. """
        return Level.CYCLE