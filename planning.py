import math
import numpy as np


class Node:
    def __init__(self, x, y, parent=None, cost=math.inf):
        self.x = x
        self.y = y
        self.xyreso = 1
        self.parent = parent
        self.cost = cost  # g(n)
        self.f_cost = math.inf  # f(n) = g(n) + h(n)

    def find_neighbors(self):
        neighbors = []
        xyreso = 1
        motion_set = [[-xyreso, 0], [0, -xyreso], [0, xyreso], [xyreso, 0]]

        for ii, m in enumerate(motion_set):
            nx = self.x + m[0]
            ny = self.y + m[1]
            # setting graph limits so as to accomodate the car in horizontal consition at the extreme righ-left or top-bottoms
            if nx > 0 and nx < 300 and ny > 0 and ny < 300:
                neighbors.append((nx, ny))
        # print('neighors = ', neighbors)
        return neighbors


def astar(start, goal, ox, oy):
    obs_list = []
    for xx, yy in zip(ox, oy):
        obs_list.append((xx, yy))

    # creating a dictionary of all nodes with integer coordinates on the graph. initial cost from goal is set to 100000 for a start heuristic calculations
    node_dict = {}
    cost_dict = {}
    for i in range(300):
        for j in range(300):
            node_dict[(i, j)] = Node(i, j)
            cost_dict[node_dict[(i, j)]] = node_dict[(i, j)].f_cost
            # cost_dict[Node(i,j)] = Node(i,j).f_cost
    edge_cost = 1
    print('node dict length - ', len(node_dict))
    # open lists indicate visited nodes but not expanded
    open_list, closed_list = [], []
    start.cost = 0
    start.f_cost = start.cost + h_cost(start, goal)
    node_dict[(start.x, start.y)].f_cost = start.f_cost
    cost_dict[start] = start.f_cost
    cost_values = list(cost_dict.values())
    min_cost = min(cost_values)
    current = list(cost_dict.keys())[list(cost_dict.values()).index(min_cost)]
    # print('start point and cost',current.x, current.y, current.cost, current.f_cost)

    current = start
    # using heapq to find node with lowest cost
    queue = []
    open_list.append(current)
    # heapq.heappush(queue, (start.f_cost, start.cost, start.x, start.y, start))
    # print(f'open_list = {len(open_list)}')
    while (len(open_list) > 0):
        cost_values = list(cost_dict.values())
        min_cost = min(cost_values)
        current = list(cost_dict.keys())[list(
            cost_dict.values()).index(min_cost)]
        # print('min_cost = ',min_cost, ' of node ', current.x, current.y)

        if (current.x == goal.x and current.y == goal.y):
            goal = current
            # print('goal found')
            path = extract_path(start, goal, node_dict)
            update = True
            return path
        # print('removing ', current.x, current.y)
        open_list.remove(current)
        neighs = current.find_neighbors()
        for neigh in neighs:
            if neigh in obs_list:
                # print('neighbor in obstacle list')
                continue
            neigh_node = node_dict[(neigh[0], neigh[1])]
            tentative_g_score = current.cost + edge_cost
            # print('current', current.x, current.y, ' ,neigh = ', neigh[0], neigh[1])
            if neigh not in closed_list:
                if tentative_g_score < cost_dict[node_dict[(neigh[0], neigh[1])]]:
                    node_dict[(neigh[0], neigh[1])].cost = tentative_g_score
                    node_dict[(neigh[0], neigh[1])
                              ].f_cost = tentative_g_score + h_cost(neigh_node, goal)
                    node_dict[(neigh[0], neigh[1])].parent = current
                    cost_dict[node_dict[(neigh[0], neigh[1])]] = node_dict[(
                        neigh[0], neigh[1])].f_cost
                    if node_dict[(neigh[0], neigh[1])] not in open_list:
                        open_list.append(node_dict[(neigh[0], neigh[1])])
                        # print('current ', current.x, current.y,', appended ', (neigh[0], neigh[1]))
        # print('popping ', current.x, current.y)
        cost_dict.pop(current)
        closed_list.append((current.x, current.y))
    print('path not found')
    return None


def extract_path(start, goal, node_dict):
    parent = goal
    path = []

    while parent != start:
        parent = goal.parent
        path.append((goal.x, goal.y))
        goal = parent
    print("Returned path")
    path = path[::-1]
    return path


def h_cost(node, goal):
    return np.sqrt((goal.x-node.x)**2 + (goal.y-node.y)**2)
