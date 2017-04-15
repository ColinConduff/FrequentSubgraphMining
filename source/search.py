
from collections import deque
from enum import IntEnum

import source.factory as factory
from source.node import Node
from source.path import Path
from source.tree import Tree
from source.cycle import Cycle

class Level(IntEnum):
    NODE = 0
    PATH = 1
    TREE = 2
    CYCLE = 3

def find_frequent_subgraphs(initial_node_fragments, min_freq, 
                            dont_generate_cycles=False, dont_generate_trees=False):
    """
    Perform level order search where: 
        level 0 contains nodes, 
        level 1 contains paths, 
        level 2 contains trees, 
        level 3 contains cycles.
    """

    frequencies = {} # {embedding_list : frequency}
    frequent_subgraphs = {} # {embedding_list: subgraph}

    levels = (Level.NODE, Level.PATH, Level.TREE, Level.CYCLE)
    queues = (deque(initial_node_fragments), deque(), deque(), deque())

    # after each queue remove infrequent fragments from source graphs

    # i = 0

    for level in levels:
        waiting = {} # {embedding_list: [fragments]} contains fragments that may be frequent

        while len(queues[level]) > 0:
            # print()
            # print("iterations: {}".format(i))
            # i += 1

            fragment = queues[level].popleft()
            embedding_list = fragment.embedding_list
            # print(embedding_list)
            subgraph = fragment.current_graph

            _update_frequencies(frequencies, embedding_list)
            _update_waiting(waiting, embedding_list, fragment)

            if _is_frequent(frequencies, embedding_list, min_freq):
                frequent_subgraphs[embedding_list] = subgraph

                for next_fragment in _next_fragments(waiting[embedding_list]):
                    queues[next_fragment.queue_level].append(next_fragment)

                del waiting[embedding_list]

    return frequent_subgraphs, frequencies

def _update_frequencies(frequencies, embedding_list):
    if embedding_list in frequencies:
        frequencies[embedding_list] += 1
    else:
        frequencies[embedding_list] = 1

def _update_waiting(waiting_list, embedding_list, fragment):
    if embedding_list not in waiting_list:
        waiting_list[embedding_list] = [fragment]
    else:
        waiting_list[embedding_list].append(fragment)

def _is_frequent(frequencies, embedding_list, min_freq):
    return frequencies[embedding_list] >= min_freq

def _next_fragments(waiting_list):
    for fragment in waiting_list:
        for edge in fragment.frontier_edges:
            next_obj = factory.apply_refinement(fragment, edge)
            if next_obj is not None:
                yield next_obj
