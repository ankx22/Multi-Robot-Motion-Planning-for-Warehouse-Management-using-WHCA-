import math
import numpy as np
import heapq


class agent:
    def __init__(x, y, start, goal, Obs_list=[]):
        self.start = start
        self.gol = goal
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.full_path = []
        self.partial_path = []
        self.g = {}
        self.f = {}
        self.h = {}
        self.open_list = []
        self.closed_list = []

    def manhatten(P1, P2):
        return abs(P1[0]-P2[0]) + abs(P1[1]-P2[1])

    def cost(self, p1, p2):
        return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

    def h_cost(self, p1, p2):
        return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

    def f_value(self, s, g, goal):
        return g + h_cost(s, goal)

    def find_neighbors(s):
        neigh_list = []
        motion_set = [[1, 0], [0, 1], [0, -1], [-1, 0]]
        for m in motion_set:
            neigh_list.append((s[0]+m[0], s[1]+m[1]))
        return neigh_list

    def RRA_Star(self):
        g[self.goal] = 0
        h[self.goal] = self.manhatten(self.goal, self.pos)

        heapq.heappush(self.open_list, (self.f_value(
            self.goal, self.g[self.goal], self.pos), self.goal))

        while Open_list:
            _, s = heapq.heappop(self.open_list)
            self.closed_list.append(s)
            if s == self.goal:
                break
            for s_n in self.find_neighbors(s):
                new_cost = g[self.start] + self.cost(self.start, s_n)
                if s_n not in Obs_list:
                    if s_n not in self.g:
                        self.g[s_n] = math.inf

                    if new_cost < self.g[s_n]:
                        self.g[s_n] = new_cost

                        Parent[s_n] = s
                        heapq.heappush(
                            Open_list, (f_value(s_n, g[s_n], goal), s_n))

        pass
