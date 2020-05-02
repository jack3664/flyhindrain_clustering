import networkx as nx
import itertools
# import matplotlib.pyplot as plot
# import community as undirected_louvain
# import louvain as directed_louvain
# import igraph as ig
from networkx.algorithms.community.centrality import girvan_newman

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

#Function to remove all the edges with a specific weight or lower
def removeEdgesWithSpecificWeight(graph, weight):
    edges = graph.edges.data(data="weight", default=1)
    edgesToRemove = []
    for edge in edges:
        if (edge[2] <= weight):
            edgesToRemove.append(edge)
    graph.remove_edges_from(edgesToRemove)
    return graph

def girvan_newman_clustering(graph):
    original_graph = graph.subgraph(sorted(nx.strongly_connected_components(graph), key=len, reverse=True)[0])
    comp = girvan_newman(original_graph)
    count = 0
#     print(tuple(sorted(c) for c in next(comp)))
    for communities in comp:
        print("1")
        print(type(communities))
        count = count + 1
        break
    
    print("Number of Communities:" + count)
#     
#     #Remove the edge weight of 1 and obtaining the strongest connected, undirected component since we know there's only one with many nodes
#     remove_1_graph = graph.subgraph(sorted(nx.strongly_connected_components(removeEdgesWithSpecificWeight(graph, 1)), key=len, reverse=True)[0])
#     comp1 = girvan_newman(remove_1_graph)
#     count1 = 0
#     print(tuple(sorted(c) for c in next(comp1)))
#     for c in next(comp1):
#         count1 = count1 + 1
#     print("Number of Communities:" + count1)
#     print("")
#     
#     #Remove the edge weights of 1 and 2 and obtaining the strongest connected, undirected component since we know there's only one with many nodes
#     remove_1_2_graph = graph.subgraph(sorted(nx.strongly_connected_components(removeEdgesWithSpecificWeight(graph, 2)), key=len, reverse=True)[0])
#     comp12 = girvan_newman(remove_1_2_graph)
#     count12 = 0
#     print(tuple(sorted(c) for c in next(comp12)))
#     for c in next(comp12):
#         count12 = count12 + 1
#     print("Number of Communities:" + count12)
#     print("")
#     
#     #Remove the edge weights of 1, 2, and 3 and obtaining the strongest connected, undirected component since we know there's only one with many nodes
#     remove_1_2_3_graph = graph.subgraph(sorted(nx.strongly_connected_components(removeEdgesWithSpecificWeight(graph, 3)), key=len, reverse=True)[0])
#     comp123 = girvan_newman(remove_1_2_3_graph)
#     count123 = 0
#     print(tuple(sorted(c) for c in next(comp123)))
#     for c in next(comp123):
#         count123 = count123 + 1
#     print("Number of Communities:" + count123)
#     print("")

def main():
    # Parse data file
    # graph = readFile(1,100000)
    graph = readFile()
    
    girvan_newman_clustering(graph)
    # G = nx.path_graph(10)
    # comp = girvan_newman(G)
    # print(tuple(sorted(c) for c in next(comp)))

if __name__ == "__main__":
    main()