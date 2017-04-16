
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
    frequent_fragments = {} # {embedding_list: fragment}

    levels = (Level.NODE, Level.PATH, Level.TREE, Level.CYCLE)
    queues = (deque(initial_node_fragments), deque(), deque(), deque())

    for level in levels:
        print(level) ###########################

        if dont_generate_trees and level == Level.TREE or \
            dont_generate_cycles and level == Level.CYCLE:
            break

        fragments_dict = {} # {embedding_list: [fragments]} contains fragments that may be frequent

        while len(queues[level]) > 0:
            fragment = queues[level].popleft()
            embedding_list = fragment.embedding_list

            _update_frequencies(frequencies, embedding_list)
            _update_fragments_dict(fragments_dict, embedding_list, fragment)

            if _is_frequent(frequencies, embedding_list, min_freq):
                frequent_fragments[embedding_list] = fragment

                for next_fragment in _next_fragments(fragments_dict[embedding_list],
                                                     dont_generate_cycles,
                                                     dont_generate_trees):
                    queues[next_fragment.queue_level].append(next_fragment)

                del fragments_dict[embedding_list]

        # The remaining fragments in fragments_dict are infrequent
        _remove_from_source_graphs(fragments_dict.values())

    return {embedding: values for (embedding, values) in _output(frequent_fragments, frequencies)}

def _output(frequent_fragments, frequencies):
    for embedding, fragment in frequent_fragments.items():
        yield embedding, (fragment.current_graph, str(fragment), frequencies[embedding])

def _update_frequencies(frequencies, embedding_list):
    if embedding_list in frequencies:
        frequencies[embedding_list] += 1
    else:
        frequencies[embedding_list] = 1

def _update_fragments_dict(fragments_dict, embedding_list, fragment):
    if embedding_list not in fragments_dict:
        fragments_dict[embedding_list] = [fragment]
    else:
        fragments_dict[embedding_list].append(fragment)

def _is_frequent(frequencies, embedding_list, min_freq):
    return frequencies[embedding_list] >= min_freq

def _next_fragments(fragments_dict, dont_generate_cycles, dont_generate_trees):
    for fragment in fragments_dict:
        for edge in fragment.frontier_edges:
            next_obj = factory.apply_refinement(fragment, edge, dont_generate_cycles, dont_generate_trees)
            if next_obj is not None:
                yield next_obj

def _remove_from_source_graphs(nested_fragments):
    for fragments in nested_fragments:
        for fragment in fragments:
            for node_id in fragment.current_graph:
                if node_id in fragment.source_graph:
                    fragment.source_graph.remove_node(node_id)
