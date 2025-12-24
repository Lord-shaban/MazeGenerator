import heapq

class Node:
    def __init__(self, x, y, g=0, h=0, parent=None):
        self.x = x
        self.y = y
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent

    def __lt__(self, other):
        return self.f < other.f


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_neighbors(node, maze):
    directions = [(0,1), (1,0), (0,-1), (-1,0)]
    neighbors = []

    for dx, dy in directions:
        nx, ny = node.x + dx, node.y + dy

        if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]):
            if maze[nx][ny] == 0:  # not a wall
                neighbors.append((nx, ny))

    return neighbors


def reconstruct_path(node):
    path = []
    while node:
        path.append((node.x, node.y))
        node = node.parent
    return path[::-1]


def a_star(maze, start, goal):
    open_list = []
    closed_set = set()
    explored = []  # <--- 1. Added list

    start_node = Node(start[0], start[1], g=0,
                      h=heuristic(start, goal))
    heapq.heappush(open_list, start_node)

    while open_list:
        current = heapq.heappop(open_list)
        explored.append((current.x, current.y)) # <--- 2. Track explored

        if (current.x, current.y) == goal:
            return reconstruct_path(current), explored # <--- 3. Return tuple

        closed_set.add((current.x, current.y))

        for nx, ny in get_neighbors(current, maze):
            if (nx, ny) in closed_set:
                continue

            g_cost = current.g + 1
            h_cost = heuristic((nx, ny), goal)
            neighbor = Node(nx, ny, g_cost, h_cost, current)

            heapq.heappush(open_list, neighbor)

    return None, explored  # <--- 4. Return tuple (even if fail)
