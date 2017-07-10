
from collections import deque

import gaston_py.factory as factory
from gaston_py.level import Level

def find_frequent_subgraphs(initial_node_fragments, min_freq,
                            dont_generate_cycles=False, dont_generate_trees=False):
    """
    Perform a level-order search for frequently occurring subgraphs.
    An iterative approach is used rather than the recursive approach used by
    the original Gaston algorithm.

    Levels:
    level 0: nodes
    level 1: paths
    level 2: trees
    level 3: cycles

    Returns:
        a dictionary of the form {embedding_list: (subgraph, graph_type, frequency)}
    """

    frequencies = {} # {embedding_list : frequency}
    frequent_fragments = {} # {embedding_list: fragment}
    visited_fragments = {} # {graph_id: set(fragments)}

    levels = (Level.NODE, Level.PATH, Level.TREE, Level.CYCLE)
    queues = (deque(initial_node_fragments), deque(), deque(), deque())

    for level in levels:

        if dont_generate_trees and level == Level.TREE or \
            dont_generate_cycles and level == Level.CYCLE:
            break

        fragments_dict = {} # {embedding_list: [fragments]}

        while len(queues[level]) > 0:

            fragment = queues[level].popleft()
            embedding_list = fragment.embedding_list

            _update_frequencies(frequencies, embedding_list)
            _update_fragments_dict(fragments_dict, embedding_list, fragment)

            if _is_frequent(frequencies, embedding_list, min_freq):
                frequent_fragments[embedding_list] = fragment

                # Generate the next fragment and
                # append it to the queue that corresponds to its graph type
                for next_fragment in _next_fragments(fragments_dict[embedding_list],
                                                     dont_generate_cycles, dont_generate_trees,
                                                     visited_fragments):
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

def _next_fragments(fragments, dont_generate_cycles, dont_generate_trees, visited_fragments):
    """
    Returns fragments that can be produced by refining previously created frequent fragments.
    """
    for prev_fragment in fragments:
        for edge in prev_fragment.frontier_edges:
            next_fragment = factory.apply_refinement(prev_fragment, edge,
                                                     dont_generate_cycles, dont_generate_trees)
            if next_fragment is not None:
                if _fragment_was_not_already_visited(visited_fragments, next_fragment):
                    yield next_fragment
                _update_visited_fragments(visited_fragments, next_fragment)

def _fragment_was_not_already_visited(visited_fragments, fragment):
    graph_id = fragment.source_graph.graph['id']
    return graph_id not in visited_fragments or fragment not in visited_fragments[graph_id]

def _update_visited_fragments(visited_fragments, fragment):
    graph_id = fragment.source_graph.graph['id']
    if graph_id in visited_fragments:
        visited_fragments[graph_id].add(fragment)
    else:
        visited_fragments[graph_id] = set([fragment])

def _remove_from_source_graphs(nested_fragments):
    for fragments in nested_fragments:
        for fragment in fragments:
            for node_id in fragment.current_graph:
                if node_id in fragment.source_graph:
                    fragment.source_graph.remove_node(node_id)
