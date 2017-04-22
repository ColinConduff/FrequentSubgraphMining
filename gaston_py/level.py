
from enum import IntEnum

class Level(IntEnum):
    """ Constants specifying the queue corresponding to the graph type. """
    NODE = 0
    PATH = 1
    TREE = 2
    CYCLE = 3
