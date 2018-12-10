# -*- coding: utf-8 -*-
"""
Created and modified by: Matthew Iglesias
80591632
Diego Aguirre 
T.A. Anitha Nath
"""

from Graph import Vertex, Graph
from EdgeWeight import EdgeWeight
from VertexSetCollection import VertexSetCollection
import heapq

def get_incoming_edge_count(edge_list, vertex):
   count = 0
   for (from_vertex, to_vertex) in edge_list:
      if to_vertex is vertex:
         count = count + 1
   return count

def topological_sort(graph):
    result_list = []

    # make list of vertices with no incoming edges.
    no_incoming = []
    for vertex in graph.adjacency_list.keys():
        if get_incoming_edge_count(graph.edge_weights.keys(), vertex) == 0:
            no_incoming.append(vertex)
    
    # remaining_edges starts with all edges in the graph.
    # A set is used for its efficient remove() method.
    remaining_edges = set(graph.edge_weights.keys())
    while len(no_incoming) != 0:
        # select the next vertex for the final result.
        current_vertex = no_incoming.pop()
        result_list.append(current_vertex)
        outgoing_edges = []

        # remove current_vertex's outgoing edges from remaining_edges.
        for to_vertex in graph.adjacency_list[current_vertex]:
            outgoing_edge = (current_vertex, to_vertex)
            if outgoing_edge in remaining_edges:
                outgoing_edges.append(outgoing_edge)
                remaining_edges.remove(outgoing_edge)
        
        # see if removing the outgoing edges creates any new vertices
        # with no incoming edges.
        for (from_vertex, to_vertex) in outgoing_edges:
            in_count = get_incoming_edge_count(remaining_edges, to_vertex)
            if in_count == 0:
                no_incoming.append(to_vertex)
    
    return result_list

# Returns a list of edges representing the graph's minimum spanning tree.
# Uses Kruskal's minimum spanning tree algorithm.
def minimum_spanning_tree(graph):
    # edge_list starts as a list of all edges from the graph
    edge_list = []
    for edge in graph.edge_weights:
        edge_weight = EdgeWeight(edge[0], edge[1], graph.edge_weights[edge])
        edge_list.append(edge_weight)
    # Turn edge_list into a priority queue (min heap)
    heapq.heapify(edge_list)

    # Initialize the collection of vertex sets
    vertex_sets = VertexSetCollection(graph.adjacency_list)

    # result_list is initially an empty list
    result_list = []

    while len(vertex_sets) > 1 and len(edge_list) > 0:
        # Remove edge with minimum weight from edge_list
        next_edge = heapq.heappop(edge_list)
        
        # set1 = set in vertex_sets containing next_edge's 'from' vertex
        set1 = vertex_sets.get_set(next_edge.from_vertex)
        # set2 = set in vertex_sets containing next_edge's 'to' vertex
        set2 = vertex_sets.get_set(next_edge.to_vertex)
        
        # If the 2 sets are distinct, then merge
        if set1 is not set2:
            # Add next_edge to result_list
            result_list.append(next_edge)
            # Merge the two sets within the collection
            vertex_sets.merge(set1, set2)

    return result_list

if __name__ == "__main__":
    # make a graph
    g = Graph()
    
    vertex_A = Vertex('A')
    vertex_B = Vertex('B')
    vertex_C = Vertex('C')
    vertex_D = Vertex('D')
    vertex_E = Vertex('E')
    vertex_F = Vertex('F')
    vertex_G = Vertex('G')
    
    g.add_vertex(vertex_A)
    g.add_vertex(vertex_B)
    g.add_vertex(vertex_C)
    g.add_vertex(vertex_D)
    g.add_vertex(vertex_E)
    g.add_vertex(vertex_F)
    g.add_vertex(vertex_G)

    g.add_directed_edge(vertex_A, vertex_B)
    g.add_directed_edge(vertex_A, vertex_C)
    g.add_directed_edge(vertex_B, vertex_F)
    g.add_directed_edge(vertex_C, vertex_D)
    g.add_directed_edge(vertex_D, vertex_F)
    g.add_directed_edge(vertex_E, vertex_F)
    g.add_directed_edge(vertex_E, vertex_G)
    g.add_directed_edge(vertex_F, vertex_G)
    
    # do topological sort on the graph
    result_list = topological_sort(g)
    
    # display sorted list
    first = True
    for vertex in result_list:
        if first:
            first = False
        else:
            print(' -> ', end='')
        print(vertex.label, end='')
    print()

# Main program 1
graph1 = Graph()

# Add vertices A through H
vertex_names = ["A", "B", "C", "D", "E", "F", "G", "H"]
for vertex_name in vertex_names:
    graph1.add_vertex(Vertex(vertex_name))

# Add edges
graph1.add_undirected_edge(graph1.get_vertex("A"), graph1.get_vertex("B"), 30)
graph1.add_undirected_edge(graph1.get_vertex("A"), graph1.get_vertex("D"), 5)
graph1.add_undirected_edge(graph1.get_vertex("B"), graph1.get_vertex("C"), 15)
graph1.add_undirected_edge(graph1.get_vertex("B"), graph1.get_vertex("D"), 11)
graph1.add_undirected_edge(graph1.get_vertex("B"), graph1.get_vertex("G"), 10)
graph1.add_undirected_edge(graph1.get_vertex("B"), graph1.get_vertex("H"), 7)
graph1.add_undirected_edge(graph1.get_vertex("C"), graph1.get_vertex("E"), 16)
graph1.add_undirected_edge(graph1.get_vertex("D"), graph1.get_vertex("E"), 8)
graph1.add_undirected_edge(graph1.get_vertex("E"), graph1.get_vertex("F"), 23)

# Get the list of edges for the graph's minimum spanning tree
tree_edges = minimum_spanning_tree(graph1)

# Display the list of edges
print("Edges in minimum spanning tree:")
for edge in tree_edges:
    print(edge.from_vertex.label + " to " + edge.to_vertex.label, end="")
    print(", weight = " + str(edge.weight))