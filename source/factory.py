
import networkx as nx

from source.node import Node
from source.path import Path
from source.tree import Tree
from source.cycle import Cycle
import source.helper as helper
import source.embedding as embedding

def create_nx_graph(origin_id, origin_label, target_id, target_label, edge_label):
    graph = nx.Graph()
    graph.add_node(origin_id, label=origin_label)
    graph.add_node(target_id, label=target_label)
    graph.add_edge(origin_id, target_id, label=edge_label)
    return nx.freeze(graph)

def extend_nx_graph(prev_graph, origin_node_id, target_node_id, node_label, edge_label):
    graph = nx.Graph(prev_graph)
    graph.add_node(target_node_id, label=node_label)
    graph.add_edge(origin_node_id, target_node_id, label=edge_label)
    return nx.freeze(graph)

def initial_nodes(graphs):
    return [Node(node_id, source_graph) for source_graph in graphs for node_id in source_graph]

def apply_refinement(fragment, edge):
    """"""
    origin_id, target_id = edge

    if isinstance(fragment, Node):
        return _create_path_from_node(fragment, target_id)
    
    elif target_id in fragment.current_graph:
        return _create_cycle(fragment, origin_id, target_id)
    
    elif isinstance(fragment, Path):
        if origin_id == fragment.back_node_id:
            return _append_to_path(fragment, target_id)
    
        elif origin_id == fragment.source_node_id:
            _prepend_node_to_path(fragment, target_id)
            # return None
    
        else:
            return _create_tree_from_path(fragment, origin_id, target_id)

    elif isinstance(fragment, Tree):
        return _create_tree_from_tree(fragment, origin_id, target_id)

def _create_path_from_node(node_fragment, appending_node_id):
    source_node_id, frontier_edges, source_graph = node_fragment

    start_node_label = source_graph.node[source_node_id]['label']
    appending_node_label = source_graph.node[appending_node_id]['label']
    edge_label = source_graph.edge[source_node_id][appending_node_id]['label']

    # Check if refinement is allowed
    if appending_node_label < start_node_label:
        return None

    current_graph = create_nx_graph(source_node_id, start_node_label, 
                                            appending_node_id, appending_node_label, 
                                            edge_label)

    # Find the embedding that begins at the previous path's back node
    # The alt embedding beginning from the new back node will be created from a different fragment
    embedding_list = embedding.create_embedding_list_if_unique(current_graph, 
                                                               source_id=source_node_id, 
                                                               alt_source_id=appending_node_id)
    if embedding_list is None:
        return None

    # total_symmetry = 0 if appending_node_label == start_node_label else 1
    
    return Path(source_node_id, appending_node_id, current_graph, 
                source_graph, embedding_list, 
                total_symmetry=0, front_symmetry=0, back_symmetry=0)

def _append_to_path(prev_path, new_back_id):

    target_node_label = prev_path.source_graph.node[new_back_id]['label']
    target_edge_label = prev_path.source_graph.edge[prev_path.back_node_id][new_back_id]['label']

    # edge1 = tuple(prev_path.embedding_list[:2]) # (l(v1), l(e1))
    # new_edge = (target_node_label, target_edge_label)
    # embedding_list = prev_path.embedding_list + (target_edge_label, target_node_label)

    # Needs to be changed if using the O(1) method for finding new path symmetries
    # total_symmetry, front_symmetry, back_symmetry = Path.new_path_symmetries(embedding_list)

    # Check if refinement is allowed
    # append is allowed if total_symmetry == 0
    # (l(v'), l(e')) > (l(v1), l(e1))
    # if (l(v'), l(e')) == (l(v1), l(e1)) and back_symmetry >= 0

    # if total_symmetry == -1 or edge1 == new_edge and back_symmetry == -1:
    #     return None

    current_graph = extend_nx_graph(prev_path.current_graph, prev_path.back_node_id, new_back_id, 
                                           target_node_label, target_edge_label)

    # Find the embedding that begins at the previous path's back node
    # The alt embedding beginning from the new back node will be created from a different fragment
    embedding_list = embedding.create_embedding_list_if_unique(current_graph, 
                                                               source_id=prev_path.source_node_id, 
                                                               alt_source_id=new_back_id)
    if embedding_list is None:
        return None
    
    return Path(prev_path.source_node_id, new_back_id, current_graph, 
                prev_path.source_graph, embedding_list, 
                total_symmetry=0, front_symmetry=0, back_symmetry=0)


def _prepend_node_to_path(prev_path, new_source_node_id):

    new_node_label = prev_path.source_graph.node[new_source_node_id]['label']
    new_edge_label = prev_path.source_graph.edge[new_source_node_id][prev_path.source_node_id]['label']

    # edge1 = tuple(prev_path.embedding_list[:2]) # (l(v1), l(e1))
    # new_edge = (new_node_label, new_edge_label)
    # embedding_list = new_edge + prev_path.embedding_list

    # Needs to be changed if using the O(1) method for finding new path symmetries
    # total_symmetry, front_symmetry, back_symmetry = Path.new_path_symmetries(embedding_list)

    # Check if refinement is allowed
    # append is allowed if total_symmetry == 1
    # (l(v'), l(e')) > (l(v1), l(e1))
    # if (l(v'), l(e')) == (l(v1), l(e1)) and back_symmetry >= 0

    # if total_symmetry != 1 or edge1 == new_edge and back_symmetry == -1:
    #     return None

    # Incorrect order if graph is directed
    current_graph = extend_nx_graph(prev_path.current_graph, prev_path.source_node_id, new_source_node_id, 
                                           new_node_label, new_edge_label)
    
    # Find the embedding that begins at the previous path's start node
    # The alt embedding beginning from the new start node will be created from a different fragment
    embedding_list = embedding.create_embedding_list_if_unique(current_graph, 
                                                               source_id=prev_path.source_node_id, 
                                                               alt_source_id=new_source_node_id)
    if embedding_list is None:
        return None
    
    return Path(new_source_node_id, prev_path.back_node_id, current_graph, 
                prev_path.source_graph, embedding_list, 
                total_symmetry=0, front_symmetry=0, back_symmetry=0)

def _create_tree_from_path(prev_path, origin_id, target_id):
    source_node_id = prev_path.source_node_id
    return _create_tree(prev_path.source_graph, prev_path.current_graph, 
                        source_node_id, prev_path.frontier_edges, 
                        origin_id, target_id)

def _create_tree_from_tree(prev_tree, origin_id, target_id):
    return _create_tree(prev_tree.source_graph, prev_tree.current_graph, 
                        prev_tree.source_node_id, prev_tree.frontier_edges, 
                        origin_id, target_id)

def _create_tree(source_graph, prev_graph, root_id, prev_frontier_edges, origin_id, target_id):
    
    new_node_label = source_graph.node[target_id]['label']
    new_edge_label = source_graph.edge[origin_id][target_id]['label']

    current_graph = extend_nx_graph(prev_graph, origin_id, target_id, 
                                           new_node_label, new_edge_label)

    embedding_list = embedding.create_embedding_list_if_unique(current_graph, 
                                                               source_id=root_id, 
                                                               alt_source_id=target_id)
    if embedding_list is None:
        return None

    return Tree(root_id, current_graph, source_graph, embedding_list)

def _create_cycle(fragment, origin_id, target_id):

    source_graph = fragment.source_graph
    prev_graph = fragment.current_graph
    source_node_id = fragment.source_node_id

    if isinstance(fragment, Path) and target_id == fragment.source_node_id:
        return None

    new_node_label = source_graph.node[target_id]['label']
    new_edge_label = source_graph.edge[origin_id][target_id]['label']

    current_graph = extend_nx_graph(prev_graph, origin_id, target_id, 
                                    new_node_label, new_edge_label)

    embedding_list = embedding.create_embedding_list_if_unique(current_graph, 
                                                               source_id=source_node_id, 
                                                               alt_source_id=target_id)
    if embedding_list is None:
        return None

    return Cycle(source_node_id, current_graph, source_graph, embedding_list)
