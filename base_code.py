import math
import matplotlib.pyplot as plt
import time
from environment import *
from planning import *
from matplotlib.patches import Rectangle as rt
from draw import draw_bot


class Node:
    def __init__(self, x, y, parent=None, cost=math.inf):
        self.x = x
        self.y = y
        self.xyreso = 5
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


class Robot:
    def __init__(self, start, goal, color='black'):
        self.start = start
        self.goal = goal
        self.start_color = color
        self.goal_color = color


def main():
    ox, oy = create_map(50, 50)
    robot_starts = [(7, 5), (44, 2)]
    robot_goals = [(14, 17), (7, 19)]
    image_path = r"C:\Users\ankit\OneDrive\Desktop\Motion planning\scripts\robot.png"
    sx, sy = [], []
    gx, gy = [], []
    for r in robot_starts:
        sx.append(r[0])
        sy.append(r[1])
    for g in robot_goals:
        gx.append(g[0])
        gy.append(g[1])

    start1 = Node(sx[0], sy[0])
    start2 = Node(sx[1], sy[1])
    print('start points are (', sx[0], ',',
          sy[0], ') and (', sx[1], ',', sy[1], ')')
    goal1 = Node(gx[0], gy[0])
    goal2 = Node(gx[1], gy[1])
    time_total = time.time()
    time1_start = time.time()

    path1 = astar(start1, goal1, ox, oy)
    time1_end = time.time()
    print('path finding time for path1 =', time1_end - time1_start)
    time2_start = time.time()
    path2 = astar(start2, goal2, ox, oy)
    time2_end = time.time()
    print('path finding time for path1 =', time2_end - time2_start)
    print('total path finding time = ', time.time()-time_total)
    print('lengths of paths = ', len(path1), len(path2))
    if (len(path1) == len(path2)):
        pass
    elif (len(path1) < len(path2)):
        diff = len(path2)-len(path1)
        temp = path1[-1]
        for i in range(diff):
            path1.append(temp)
    else:
        diff = len(path1)-len(path2)
        temp = path2[-1]
        for i in range(diff):
            path2.append(temp)
    path1_x, path1_y, path2_x, path2_y = [], [], [], []

    for i in range(len(path1)):
        path1_x.append(path1[i][0])
        path1_y.append(path1[i][1])
        path2_x.append(path2[i][0])
        path2_y.append(path2[i][1])

    for i in range(len(path1)):
        plt.cla()
        plt.plot(ox, oy, 'sk')
        plt.plot(sx, sy, 'sg')
        plt.plot(gx, gy, 'sr')
        plt.plot(path1_x, path1_y, 'r')
        plt.plot(path2_x, path2_y, 'b')
        draw_bot(path1_x[i], path1_y[i], image_path)
        draw_bot(path2_x[i], path2_y[i], image_path)

        plt.axis('equal')
        plt.show(block=False)
        plt.pause(0.001)

    plt.plot(ox, oy, 'sk')
    plt.show()


if __name__ == "__main__":
    main()
