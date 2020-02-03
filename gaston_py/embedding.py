
def create_embedding_list(graph, source_id):
    """ Generalized, slow method for creating unique embedded lists for any type of graph. """
    embedding_labels = [graph.node[source_id]['label']]
    embed_iter = _create_embedding_list(graph, visited=set(), node_id=source_id)

    for node_id, (edge_label, neighbor_label) in embed_iter:
        embedding_labels.append(edge_label)
        embedding_labels.append(neighbor_label)

    return tuple(embedding_labels)

def create_embedding_list_if_unique(graph, source_id, alt_source_id):
    node_label = graph.nodes[source_id]['label']
    alt_node_label = graph.nodes[alt_source_id]['label']

    if node_label > alt_node_label:
        return None

    # If a cycle is formed by wrapping back to source_id, source_id == alt_source_id
    elif node_label < alt_node_label or source_id == alt_source_id:
        return create_embedding_list(graph, source_id)
    else:
        return _embedding_list_with_comparison(graph, source_id, alt_source_id, node_label, alt_node_label)

def _embedding_list_with_comparison(graph, source_id, alt_source_id, node_label, alt_node_label):

    embedding_list = [node_label]
    source_node_ids = [source_id]
    alt_node_ids = [alt_source_id]

    embed_iter = _create_embedding_list(graph, visited=set(), node_id=source_id)
    alt_embed_iter = _create_embedding_list(graph, visited=set(), node_id=alt_source_id)

    should_compare = True

    while True:
        try:
            node_id, edge = next(embed_iter)
            embedding_list.extend(edge)

            if should_compare:
                alt_node_id, alt_edge = next(alt_embed_iter)

                source_node_ids.append(node_id)
                alt_node_ids.append(alt_node_id)

                if edge > alt_edge:
                    return None
                elif edge < alt_edge:
                    should_compare = False
                    del source_node_ids
                    del alt_node_ids

        except StopIteration:
            break

    if should_compare and source_node_ids > alt_node_ids:
        return None

    return tuple(embedding_list)

def _create_embedding_list(graph, visited, node_id):
    for edge_label, neighbor_label, neighbor_id in sorted(_neighbor_labels(graph, visited, node_id)):
        if (node_id, neighbor_id) not in visited:
            visited.add((node_id, neighbor_id))
            visited.add((neighbor_id, node_id)) # if graph is undirected

            yield node_id, (edge_label, neighbor_label)
            yield from _create_embedding_list(graph, visited, neighbor_id)

def _neighbor_labels(graph, visited, node_id):
    for neighbor_id in graph.neighbors(node_id):
        if (node_id, neighbor_id) not in visited:
            edge_label = graph[node_id][neighbor_id]['label']
            neighbor_label = graph.nodes[neighbor_id]['label']
            yield edge_label, neighbor_label, neighbor_id
