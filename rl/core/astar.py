import heapq

inf = float("inf")

class VertexInfo:
    def __init__(self, vertex, to_start=inf, to_goal=inf, edge=None):
        self.vertex = vertex
        self.to_start = to_start
        self.to_goal = to_goal
        self.edge = edge

    def __lt__(self, x):
        return self.to_goal < x.to_goal

def a_star(graph, start, goal, heuristic):
    # queued vertices
    open_set = []
    vertex_mapper = {}

    # visited vertices
    closed_set = {}
   
    start_info = VertexInfo(start, 0, heuristic(start, goal))
    open_set.append(start_info)
    vertex_mapper[start] = start_info

    while len(open_set) > 0:
        vertex_info = heapq.heappop(open_set)
        vertex = vertex_info.vertex

        # mark vertex visited
        closed_set[vertex] = vertex_info

        if vertex == goal:
            return reconstruct_path(closed_set, goal)

        need_heapify = False
        for pair in graph[vertex]:
            neighbor, cost = pair
            neighbor_info = vertex_mapper.setdefault(neighbor,
                    VertexInfo(neighbor))
                
            if neighbor in closed_set:
                continue

            neighbor_info = vertex_mapper[neighbor]
            total_cost = vertex_info.to_start + cost
            current_cost = neighbor_info.to_start
            if neighbor_info not in open_set:
                neighbor_info.to_start = total_cost
                neighbor_info.to_goal = total_cost + heuristic(neighbor, goal)
                neighbor_info.edge = vertex
                heapq.heappush(open_set, neighbor_info)
            elif total_cost < neighbor_info.to_start:
                neighbor_info.to_start = total_cost
                neighbor_info.to_goal = total_cost + heuristic(neighbor, goal)
                neighbor_info.edge = vertex
                need_heapify = True

        if need_heapify:
            heapq.heapify(open_set)

    return None

def reconstruct_path(closed_set, goal):
    path = [goal]
    current = goal
    while current != None:
        next = closed_set[current].edge
        if next == None:
            break
        path.append(next)
        current = next

    return list(reversed(path))

