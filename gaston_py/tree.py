
from gaston_py.fragment import Fragment
from gaston_py.level import Level

class Tree(Fragment):
    """ A fragment containing a tree subgraph. """

    def __str__(self):
        return "Tree"

    @property
    def queue_level(self):
        """ A property to specify the search queue containing tree fragments. """
        return Level.TREE
