from collections import defaultdict
import heapq

class VertexInfo:
    def __init__(self, vertex, cost=float("inf"), edge=None):
        self.vertex = vertex
        self.cost = cost
        self.edge = edge

    def __lt__(self, x):
        return self.cost < x.cost

"""Finds minimal spanning tree given adjacency list"""
def find_minimal_spanning_tree(graph, starting=None):
    if len(graph.keys()) == 0:
        return {}
    
    if starting is None:
        starting = graph.keys()[0]

    # tree/forest so far
    forest = {}
    
    # vertices waiting to be added, ordered by cost to add
    # vertex info contains (vertex, cost to add, edge realizing cost)
    vertex_mapper = {vertex:VertexInfo(vertex) for vertex in graph}
    vertex_mapper[starting].cost = 0
    pqueue = vertex_mapper.values()
    heapq.heapify(pqueue)

    while len(pqueue) > 0:
        # fetch cheapest vertex
        vertex_info = heapq.heappop(pqueue)
        vertex = vertex_info.vertex

        # add to forest
        forest[vertex] = vertex_info.edge

        # update neighbors
        for pair in graph[vertex]:
            neighbor, cost = pair
            if neighbor in forest:
                continue
            neighbor_info = vertex_mapper[neighbor]
            if cost < neighbor_info.cost:
                neighbor_info.cost = cost
                neighbor_info.edge = vertex
                # update heap
                heapq.heapify(pqueue)

    return forest

