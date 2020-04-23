import networkx as nx
import matplotlib.pyplot as plot
import community as undirected_louvain
import louvain as directed_louvain
import igraph as ig

#Function used to the read the file containing the edges/nodes on the FlyHindrain network
def readFile(start_line_idx=0, read_n_lines=-1):
    graph = nx.DiGraph()
    weighted_edges = []

    with open("traced_total_connections.txt", "r") as file:
        count = 0
        for line in file:
            if read_n_lines > 0 and count > start_line_idx + read_n_lines:
                break

            if line[0] != '#' and count >= start_line_idx:
                tokens = line.split()
                weighted_edges.append((int(tokens[0]), int(tokens[1]), float(tokens[2])))

            count += 1

    graph.add_weighted_edges_from(weighted_edges)
    
    return graph

#Function to read the file containing the edges excluding those with weights 1
def readFileExcludingWeights1(start_line_idx=0, read_n_lines=-1):
    graph = nx.DiGraph()
    weighted_edges = []

    with open("traced_total_connections.txt", "r") as file:
        count = 0
        for line in file:
            if read_n_lines > 0 and count > start_line_idx + read_n_lines:
                break

            if line[0] != '#' and count >= start_line_idx:
                tokens = line.split()
                if (float(tokens[2]) != 1):
                    weighted_edges.append((int(tokens[0]), int(tokens[1]), float(tokens[2])))

            count += 1

    graph.add_weighted_edges_from(weighted_edges)
    
    return graph

#Function to read the file containing the edges excluding those with weights 2
def readFileExcludingWeights2(start_line_idx=0, read_n_lines=-1):
    graph = nx.DiGraph()
    weighted_edges = []

    with open("traced_total_connections.txt", "r") as file:
        count = 0
        for line in file:
            if read_n_lines > 0 and count > start_line_idx + read_n_lines:
                break

            if line[0] != '#' and count >= start_line_idx:
                tokens = line.split()
                if (float(tokens[2]) != 2):
                    weighted_edges.append((int(tokens[0]), int(tokens[1]), float(tokens[2])))

            count += 1

    graph.add_weighted_edges_from(weighted_edges)
    
    return graph

#Y-axis is the Fraction of Edges that has a certain weight. X-axis is are the weights: 1-10, 10-20, etc
def fractionOfEdgesOverWeightGraph(graph):
    edges_1 = [(u, v) for (u, v, d) in graph.edges(data=True) if (d['weight'] == 1)]
    edges_2_to_4 = [(u, v) for (u, v, d) in graph.edges(data=True) if (d['weight'] > 1 and d['weight'] <= 4)]
    edges_5_to_10 = [(u, v) for (u, v, d) in graph.edges(data=True) if (d['weight'] > 4 and d['weight'] <= 10)]
    edges_11_to_20 = [(u, v) for (u, v, d) in graph.edges(data=True) if (d['weight'] > 10 and d['weight'] <= 20 )]
    edges_21_to_30 = [(u, v) for (u, v, d) in graph.edges(data=True) if (d['weight'] > 20 and d['weight'] <= 30 )]
    edges_31_to_40 = [(u, v) for (u, v, d) in graph.edges(data=True) if (d['weight'] > 30 and d['weight'] <= 40 )]
    edges_41_to_50 = [(u, v) for (u, v, d) in graph.edges(data=True) if (d['weight'] > 40 and d['weight'] <= 50 )]
    edges_51_to_60 = [(u, v) for (u, v, d) in graph.edges(data=True) if (d['weight'] > 50 and d['weight'] <= 60 )]
    edges_61_to_100 = [(u, v) for (u, v, d) in graph.edges(data=True) if (d['weight'] > 60 and d['weight'] <= 100 )]
    
    total_edges = float(len(graph.edges()))
    y_values = [round(len(edges_1)/total_edges, 4), round(len(edges_2_to_4)/total_edges, 4), round(len(edges_5_to_10)/total_edges, 4), round(len(edges_11_to_20)/total_edges, 4), 
                round(len(edges_21_to_30)/total_edges, 4), round(len(edges_31_to_40)/total_edges, 4), round(len(edges_41_to_50)/total_edges, 4), 
                round(len(edges_51_to_60)/total_edges, 4), round(len(edges_61_to_100)/total_edges, 4)]
    
    fig = plot.figure()
    plot.xticks(range(9), ["1", "2-4", "5-10", "11-20", "21-30", "31-40", "41-50", "51-60", "61-100"])
    
    plot.xlabel("Weights of edges")
    plot.ylabel("Fraction of Edges")
    plot.title("Fraction of edges with ranges of weights")
    show = fig.add_subplot(111)
    
    plot.bar(range(9), y_values)
    for i, j in zip(range(9), y_values):
        show.annotate(str(j), xy=(i-0.4, j+0.005))
    
    plot.show()

# Y-axis is the number of nodes. X-axis is the degree of In degrees 
def nodesOverInDegrees(graph):
    in_degrees = graph.in_degree()
    in_degree_count = dict()

    # out_degree is a tuple of (node, out_degree)
    for in_degree in in_degrees:
        in_degree_count[in_degree[1]] = in_degree_count.get(in_degree[1], 0) + 1

    x_values, y_values = list(zip(*sorted(in_degree_count.items())))
    number_of_bars = len(x_values)
    plot.bar(range(number_of_bars), y_values)
    plot.show()

# Y-axis is the number of nodes. X-axis is the degree of Out degrees 
def nodesOverOutDegrees(graph):
    out_degrees = graph.out_degree()
    out_degree_count = dict()

    # out_degree is a tuple of (node, out_degree)
    for out_degree in out_degrees:
        out_degree_count[out_degree[1]] = out_degree_count.get(out_degree[1], 0) + 1

    x_values, y_values = list(zip(*sorted(out_degree_count.items())))
    number_of_bars = len(x_values)
    plot.bar(range(number_of_bars), y_values)
    plot.show()
    
def nodesOverWeightOfInDegrees(graph):
    bucket_ranges = [(1,100), (101,200), (201,300), (301,400), (401,500), (501,600), (601,700), (701,800), (801, 900)]
    bucket_values = []

    for bucket_range in bucket_ranges:
        bucket_value = len([node for node in graph.nodes if graph.in_degree(node, weight='weight') >= bucket_range[0] and graph.out_degree(node, weight='weight') <= bucket_range[1]])
        bucket_values.append(bucket_value)
        # print("Nodes from {0} to {1}: {2}".format(bucket_range[0], bucket_range[1], bucket_value))
    
    leftover_bucket = len([node for node in graph.nodes if graph.in_degree(node, weight='weight') >= bucket_ranges[-1][1] + 1])
    bucket_values.append(leftover_bucket)
    # print("Nodes from {0} to n: {1}".format(bucket_ranges[-1][1] + 1, leftover_bucket))

    bucket_labels = ["{0}-{1}".format(bucket_range[0], bucket_range[1]) for bucket_range in bucket_ranges]
    bucket_labels.append("{0}+".format(bucket_ranges[-1][1] + 1))

    # print(bucket_labels)
    # print(bucket_values)

    fig = plot.figure()
    plot.xticks(range(len(bucket_labels)), bucket_labels)
    
    plot.xlabel("Weighted in-degree of nodes")
    plot.ylabel("Number of nodes")
    plot.title("Number of nodes with ranges of weighted in-degree")
    
    plot.bar(range(len(bucket_labels)), bucket_values)
    
    plot.show()

    
def nodesOverWeightOfOutDegrees(graph):
    bucket_ranges = [(1,100), (101,200), (201,300), (301,400), (401,500), (501,600), (601,700), (701,800), (801, 900)]
    bucket_values = []

    for bucket_range in bucket_ranges:
        bucket_value = len([node for node in graph.nodes if graph.out_degree(node, weight='weight') >= bucket_range[0] and graph.out_degree(node, weight='weight') <= bucket_range[1]])
        bucket_values.append(bucket_value)
        # print("Nodes from {0} to {1}: {2}".format(bucket_range[0], bucket_range[1], bucket_value))
    
    leftover_bucket = len([node for node in graph.nodes if graph.out_degree(node, weight='weight') >= bucket_ranges[-1][1] + 1])
    bucket_values.append(leftover_bucket)
    # print("Nodes from {0} to n: {1}".format(bucket_ranges[-1][1] + 1, leftover_bucket))

    bucket_labels = ["{0}-{1}".format(bucket_range[0], bucket_range[1]) for bucket_range in bucket_ranges]
    bucket_labels.append("{0}+".format(bucket_ranges[-1][1] + 1))

    fig = plot.figure()
    plot.xticks(range(len(bucket_labels)), bucket_labels)
    
    plot.xlabel("Weighted out-degree of nodes")
    plot.ylabel("Number of nodes")
    plot.title("Number of nodes with ranges of weighted out-degree")
    
    plot.bar(range(len(bucket_labels)), bucket_values)
    
    plot.show()
    
#Running Louvain on undirected version of the graph
def louvain_clustering_undirected(graph):
    partition = undirected_louvain.best_partition(graph)
    
    #drawing
    pos = nx.spring_layout(graph)
    count = 0.
    size_of_communities = []
    for com in set(partition.values()):
        count = count + 1.
        list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
        size_of_communities.append(len(list_nodes))
    print(size_of_communities)
    nx.draw_networkx_nodes(graph, pos, alpha=0.5, node_size=5)
    plot.show()

#Running Louvain on directed version of the graph
def louvain_clustering_directed(graph):
    #Need implementation, use the package for louvain directed
    print("Directed louvain")

def main():
    # Parse data file
    # graph = readFile(1,100000)
    graph = readFile()
    
    # Generate graphs
#     fractionOfEdgesOverWeightGraph(graph)
#     nodesOverInDegrees(graph)
#     nodesOverOutDegrees(graph)
#     nodesOverWeightOfInDegrees(graph)
#     nodesOverWeightOfOutDegrees(graph)

    #This only removes like 50 nodes and there's only one strongly connected component, can't generate ten
    strongest_connected_graph = graph.subgraph(sorted(nx.strongly_connected_components(graph), key=len, reverse=True)[0])
    
    #Converting networkx to igraph to be used in directed louvain algorithm
    igraph_directed = ig.Graph.Adjacency(nx.to_numpy_matrix(strongest_connected_graph) > 0).tolist()
    
    #Test clustering algorithms on the undirected strongly connected graphn
    undirected_version_graph = strongest_connected_graph.to_undirected()
    louvain_clustering_undirected(undirected_version_graph)

if __name__ == "__main__":
    main()
