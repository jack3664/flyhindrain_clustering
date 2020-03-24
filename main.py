import networkx as nx
import matplotlib.pyplot as plot
import numpy as np

#Function used to the read the file containing the edges/nodes on the FlyHindrain network
def readFile():
    file = open("traced_total_connections.txt", "r")
    graph = nx.read_weighted_edgelist(file, nodetype=int, create_using=nx.DiGraph())
    file.close()
    return graph

#Y-axis is the Fraction of Edges that has a certain weight. X-axis is are the weights: 1-10, 10-20, etc
def fractionOfEdgesOverWeightGraph():
    graph = readFile()
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
    
def nodesOverInDegrees():
    graph = readFile()
    print("Y-axis is the number of nodes. X-axis is the degree of In degrees")
    
def nodesOverOutDegrees():
    graph = readFile()
    print("Y-axis is the number of nodes. X-axis is the degree of Out degrees")
    
def nodesOverWeightOfInDegrees():
    graph = readFile()
    print("Y-axis is the number of nodes. X-axis is the weight of In degrees (can probably be 1-10, 10-20, etc. Experiment I guess")
    
def nodesOverWeightOfOutDegrees():
    graph= readFile()
    print("Y-axis is the number of nodes. X-axis is the weight of Out degrees (can probably be 1-10, 10-20, etc. Experiment I guess")
    
fractionOfEdgesOverWeightGraph()