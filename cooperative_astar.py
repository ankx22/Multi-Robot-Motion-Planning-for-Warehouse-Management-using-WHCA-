from astar import *
import math
import numpy
from draw import draw_bot, draw_endpoint
import matplotlib.pyplot as plt
import time

# David Silver's paper's understanding:
# Find A-star optimal paths for all robots. Check for a window of first 8 steps if a robot is colliding with any robot. If yes, reroute as per priority to each robot
# Start travel. When robot has reached halfway in the 4 steps, it checks its updated trajectory for next windoe of 8 steps. Priority can be decided based on RRAStar algorithm


def update_time_dict(time_keys, path):
    new_time_keys = time_a_star(path)
    old_keys = time_keys.copy()
    for key in new_time_keys:
        old_keys.append(key)
    return old_keys


def reroute_window(path, index, goal_list, ox, oy):
    pass


def update_path(time_keys, path, ox, oy):
    temp_ox = ox.copy()
    temp_oy = oy.copy()
    k = 0
    print('timed keys = ', time_keys)

    while k < len(path):
        if (path[k][0], path[k][1], k) in time_keys:
            print(f"key {path[k][0], path[k][1], k} already occupied")
            path.insert(k, (path[k-1][0], path[k-1][1]))
            k = 0
            continue
        k += 1

    for i in range(len(path)):
        if (path[i][0], path[i][1], i-1) in time_keys and (path[i-1][0], path[i-1][1], i) in time_keys:
            print('path intersection at',
                  path[i-1][0], path[i-1][1], i-1, ' and ', path[i][0], path[i][1], i)
            path.insert(i-2, (path[i-3][0], path[i-3][1]))
            path.insert(i-2, (path[i-3][0], path[i-3][1]))
            path.insert(i-2, (path[i-3][0], path[i-3][1]))

    return path


def plot_path_update(path_list):
    n = len(path_list)
    len_list = [len(path) for path in path_list]
    for path in path_list:
        diff = max(len_list) - len(path)
        if diff != 0:
            for k in range(diff):
                path.append(path[-1])

    len_list = [len(path) for path in path_list]

    return path_list


def make_obs(ox, oy):
    for i in range(15, 21):
        ox.append(i)
        oy.append(12)

    for i in range(15, 22):
        ox.append(i)
        oy.append(19)

    for i in range(12, 19):
        oy.append(i)
        ox.append(15)

    for i in range(12, 19):
        oy.append(i)
        ox.append(21)
    return ox, oy


def main():
    start_pts = [(7, 5), (5, 5), (1, 6), (15, 22), (14, 12),
                 (21, 20), (19, 3)]  # , (25,20),(4,12)]
    goal_pts = [(5, 8), (7, 8), (8, 17), (3, 10), (12, 4),
                (2, 2), (3, 13)]  # , (4,20),(25,20)]

    start_pts = [(7, 5), (5, 5), (21, 20)]
    goal_pts = [(5, 8), (7, 8), (2, 2)]

    ox, oy = [], []
    path_list = []
    ox, oy = make_obs(ox, oy)
    # store goal reaching time
    goal_times = []
    for i in range(len(start_pts)):
        # calculate shortest path
        path = astar(start_pts[i], goal_pts[i], ox, oy)
        if (i == 0):
            # create a robot coordinate list with (x,y,t)
            timed_keys = time_a_star(path)
            goal_times.append((path[-1][0], path[-1][1], len(path)-1))
        else:
            # update path to avoid collision with prev robots paths
            path = update_path(timed_keys, path, ox, oy)
            timed_keys = update_time_dict(timed_keys, path)
            goal_times.append((path[-1][0], path[-1][1], len(path)-1))
        # create a path lists for plotting
        path_list.append(path)
        path_all = plot_path_update(path_list)

    print('path list = ', path_list[0])
    print('goal reached list ', goal_times)
    # for paths in path_list:
    # print(paths)
    # -------------------------------------- start of plotting -----------------------------------------------
    image_path = r"C:\Users\ankit\OneDrive\Desktop\Motion planning\scripts\robot.png"
    vis = 1
    if vis:
        for i in range(len(path_all[0])):
            plt.cla()
            plt.plot(ox, oy, 'sk')
            for start, goal in zip(start_pts, goal_pts):
                draw_endpoint(start, 'orange')
                draw_endpoint(goal, 'grey')

            for path_n in path_all:
                draw_bot(path_n[i][0], path_n[i][1], image_path)
                print(path_n[i][0], path_n[i][1], i, end=', ')
            print('\n')
            plt.axis('equal')
            plt.xlim([-5, 30])
            plt.ylim([-5, 30])

            # plt.show(block=False)
            plt.pause(0.5)
    # plt.show()
    # abstract distace of any point from a goal point
    x = (24, 24)
    y = AbstractDist(x, goal_pts[-1], ox, oy)


if __name__ == "__main__":
    main()
