import functools
import networkx as nx
import matplotlib.pyplot as plt

def draw_nx_graphs(graphs):
    for graph in graphs:
        nx.draw_networkx(graph)
        # nx.draw_networkx_labels(graph)
        plt.show()

def create_nx_node_graph(source_node_id, node_label):
    current_graph = nx.Graph()
    current_graph.add_node(source_node_id, label=node_label)
    return nx.freeze(current_graph)

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

def read_line_graphs(file_path):
    """
    Returns a list of NetworkX graph objects read from a line graph file.
    """
    graph_map = {}

    with open(file_path, "r") as f:
        graph_id = 0

        for line in f:
            line = line.strip()
            characters = line.split(" ")

            if line.startswith("t #"):
                graph_id += 1
                graph = nx.Graph(id=graph_id, embeddings=[])
                graph_map[graph_id] = graph

            elif line.startswith("v"):
                label = " ".join(characters[2:]).strip('\'')
                graph_map[graph_id].add_node(characters[1], label=label)

            elif line.startswith("e"):
                label = " ".join(characters[3:]).strip('\'')
                graph_map[graph_id].add_edge(characters[1], characters[2], label=label)

            elif line.startswith("#=>"):
                embedding = characters[1]
                graph_map[graph_id].graph['embeddings'].append(embedding)

    return graph_map.values()

def write_line_graphs(graphs, file_path):
    """ Write line graphs to file path. """
    with open(file_path, "w") as f:
        for g_id, graph in enumerate(graphs):
            if "id" in graph.graph:
                f.write("t # {}\n".format(graph.graph['id']))
            else:
                f.write("t # {}\n".format(g_id))

            node_dict = {}

            for index, (node_id, data) in enumerate(graph.nodes_iter(data=True)):
                node_dict[node_id] = index
                node_label = data['label']
                f.write("v {} {}\n".format(index, node_label))

            for source, target, data in graph.edges_iter(data=True):
                f.write("e {} {} {}\n".format(node_dict[source], node_dict[target], data['label']))

def count_total_nodes(graphs):
    return functools.reduce(lambda total, graph: total + graph.number_of_nodes(), graphs, 0)

def count_total_edges(graphs):
    return functools.reduce(lambda total, graph: total + graph.number_of_edges(), graphs, 0)

def count_unique_nodes(graphs):
    return len(set(data['label'] for graph in graphs for _, data in graph.nodes_iter(data=True)))

def count_unique_edges(graphs):
    return len(set(edge['label'] for graph in graphs for _, _, edge in graph.edges_iter(data=True)))
