import networkx as nx
import matplotlib.pyplot as plot
import numpy as np

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
def nodesOverInDegrees():
    graph = readFile()
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
def nodesOverOutDegrees():
    graph = readFile()
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
    # nodes_1_to_10 = []
    print("Y-axis is the number of nodes. X-axis is the weight of In degrees (can probably be 1-10, 10-20, etc. Experiment I guess")
    
# Y-axis is the number of nodes. X-axis is the weight of Out degrees.
def nodesOverWeightOfOutDegrees():
    graph = readFile()
    n = nx.nodes(graph)
    counters = {}
    for i in n:
        out = graph.out_degree(i)
        if out in counters:
            counters[out] += 1
        counters.update({out: 1})
        
    # print(counters)
    print(len(counters))
    print(nx.number_of_nodes(graph))


def main():
    # Parse data file
    # graph = readFile(1,100)
    graph = readFile()
    
    # Generate graphs
    # fractionOfEdgesOverWeightGraph()
    nodesOverInDegrees()
    nodesOverOutDegrees()
    # nodesOverWeightOfInDegrees()
    # nodesOverWeightOfOutDegrees()

if __name__ == "__main__":
    main()
