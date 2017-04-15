
from collections import deque
import source.factory as factory

def find_frequent_subgraphs(initial_fragments, min_freq):

    # combine these into a namedtuple
    frequencies = {} # {embedding_list : frequency}
    frequent_subgraphs = {} # {embedding_list: subgraph}
    waiting = {} # {embedding_list: [fragments]}

    queue = deque(initial_fragments)

    # i = 0

    while len(queue) > 0:
        # print()
        # print("iterations: {}".format(i))
        # i += 1

        fragment = queue.popleft()
        embedding_list = fragment.embedding_list
        # print(embedding_list)
        subgraph = fragment.current_graph

        _update_frequencies(frequencies, embedding_list)
        _update_waiting(waiting, embedding_list, fragment)

        if _is_frequent(frequencies, embedding_list, min_freq):
            frequent_subgraphs[embedding_list] = subgraph
            queue.extend(_next_fragment(waiting[embedding_list]))
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

def _next_fragment(waiting_list):
    for fragment in waiting_list:
        for edge in fragment.frontier_edges:
            next_obj = factory.apply_refinement(fragment, edge)
            if next_obj is not None:
                yield next_obj
