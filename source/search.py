
import source.factory as factory

def find_frequent_subgraphs(initial_gaston_objects, min_freq):

    # combine these into a namedtuple
    frequencies = {} # {embedding_list : frequency}
    frequent_subgraphs = {} # {embedding_list: subgraph}
    waiting = {} # {embedding_list: [gaston_objects]}

    current_level = initial_gaston_objects

    i = 0

    # level order search
    while len(current_level) > 0 and i < 5:
        next_level = []

        print()
        print("iterations: {}".format(i))
        i += 1

        print(set(type(gaston_obj) for gaston_obj in current_level))

        for gaston_obj in current_level:
            embedding_list = gaston_obj.embedding_list
            print(embedding_list)
            subgraph = gaston_obj.current_graph

            _update_frequencies(frequencies, embedding_list)
            _update_waiting(waiting, embedding_list, gaston_obj)

            if _is_frequent(frequencies, embedding_list, min_freq):
                frequent_subgraphs[embedding_list] = subgraph
                next_level.extend(_next_gaston_object(waiting[embedding_list]))
                waiting[embedding_list] = []

        current_level = next_level

    return frequent_subgraphs, frequencies

def _update_frequencies(frequencies, embedding_list):
    if embedding_list in frequencies:
        frequencies[embedding_list] += 1
    else:
        frequencies[embedding_list] = 1

def _update_waiting(waiting_list, embedding_list, gaston_obj):
    if embedding_list not in waiting_list:
        waiting_list[embedding_list] = [gaston_obj]
    else:
        waiting_list[embedding_list].append(gaston_obj)

def _is_frequent(frequencies, embedding_list, min_freq):
    return frequencies[embedding_list] > min_freq

def _next_gaston_object(waiting_list):
    for gaston_obj in waiting_list:
        for edge in gaston_obj.frontier_edges:
            next_obj = factory.apply_refinement(gaston_obj, edge)
            if next_obj is not None:
                yield next_obj
