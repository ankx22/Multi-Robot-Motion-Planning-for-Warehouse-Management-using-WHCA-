from astar import *
import math
import numpy
from draw import draw_bot, draw_endpoint
import matplotlib.pyplot as plt
import time
from warehouse import *
# David Silver's paper's understanding:
# Find A-star optimal paths for all robots. Check for a window of first 8 steps if a robot is colliding with any robot. If yes, reroute as per priority to each robot
# Start travel. When robot has reached halfway in the 4 steps, it checks its updated trajectory for next windoe of 8 steps. Priority can be decided based on RRAStar algorithm
image_path = "robot.png"


def update_time_dict(time_keys, path):
    new_time_keys = time_a_star(path)
    old_keys = time_keys.copy()
    for key in new_time_keys:
        old_keys.append(key)
    return old_keys


def update_path(time_keys, path, ox, oy):
    temp_ox = ox.copy()
    temp_oy = oy.copy()
    k = 0
    # print('timed keys = ', time_keys)

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


def make_8_step_path(path, window_size):
    if len(path) % window_size != 0:
        while len(path) % window_size != 0:
            path.append(path[-1])
    return path


def time_coord(path, start_index, end_index):
    timed_coord = []
    for i in range(start_index, end_index):
        timed_coord.append((path[i-start_index][0], path[i-start_index][1], i))
    return timed_coord


def reroute_window(path1, path2, start_index, end_index, ox, oy):
    flag = False  # Flag will stay false if there is no collision
    temp_ox = ox.copy()
    temp_oy = oy.copy()
    time_keys = time_coord(path1, start_index, end_index)
    window_size = 8
    # print(f'length of path2 = {len(path2)}')
    print(f'\npath1 = ', path1, '\n')
    for i in range(start_index, end_index):
        print("index = ", i)
        if (path2[i][0], path2[i][1], i) in time_keys:
            index = i
            print('intersection at', path2[i][0], path2[i][1], index)
            print('remaining path of path1 = ', path1[i-start_index:])
            temp = path2[:(i-1)]
            flag = True
            break
    # new route avoiding remaining of the path1
    if flag:
        print('path1 index = ', index-start_index,
              '\npath before collision = ', temp)
        for i in range(index-start_index, len(path1)):
            temp_ox.append(path1[i][0])
            temp_oy.append(path1[i][1])
        new_start = path2[index-1]
        new_goal = path2[-1]
        print('new start = ', new_start, ', new_goal = ', new_goal, ', i = ', i)
        new_path = astar(new_start, new_goal, temp_ox, temp_oy)
        print('new path = ', new_path)
        print(f'length of temp = {len(temp)}')
        for point in new_path:
            temp.append(point)
        print(f'length of temp = {len(temp)} \n{temp}')
        return temp
    else:
        print("No collision")
        return path2


def reroute_window2(prev_path_list, path2, start_index, end_index, ox, oy):
    flag = False  # Flag will stay false if there is no collision
    temp_ox = ox.copy()
    temp_oy = oy.copy()

    # time_keys = time_coord(path1, start_index, end_index)
    time_keys = []
    for path in prev_path_list:
        time_keys_for_path = time_coord(
            path[start_index:end_index], start_index, end_index)
        for key in time_keys_for_path:
            time_keys.append(key)
    window_size = 8
    # print(f'length of path2 = {len(path2)}')
    # print(f'\npath1 = ', path1,'\n')
    for i in range(start_index, end_index):
        # print("index = ", i)
        if (path2[i][0], path2[i][1], i) in time_keys:
            index = i
            print('intersection at', path2[i][0], path2[i][1], index)
            # print('remaining path of path1 = ', path1[i-start_index:])
            temp = path2[:(i-1)]
            flag = True
            break
    # new route avoiding remaining of the path1
    if flag:
        print('path1 index = ', index-start_index,
              '\npath before collision = ', temp)
        for path in prev_path_list:
            for i in range(index-start_index, len(path)):
                temp_ox.append(path[i][0])
                temp_oy.append(path[i][1])
        new_start = path2[index-1]
        new_goal = path2[-1]
        print('new start = ', new_start, ', new_goal = ', new_goal, ', i = ', i)
        new_path = astar(new_start, new_goal, temp_ox, temp_oy)
        print('new path = ', new_path)
        print(f'length of temp = {len(temp)}')
        for point in new_path:
            temp.append(point)
        print(f'length of temp = {len(temp)} \n{temp}')
        return temp
    else:
        # print("No collision")
        return path2


def main():
    # original start and goals for demonstrating windowed heirarchial A-star algorithm
    # start_pts = [(5,5), (21,20), (2,20)]
    # goal_pts = [(7,8), (2,2), (20,5)]

    start_pts = [(5, 5), (21, 20), (2, 20), (21, 40)]
    goal_pts = [(7, 8), (2, 2), (20, 5), (31, 10)]

    start_pts = [(5, 25), (19, 25), (35, 25), (10, 23)]
    goal_pts = [(35, 39), (38, 35), (8, 35), (22, 37)]

    ox, oy = [], []
    path_list = []
    ox, oy = make_obs(ox, oy)
    path1 = astar(start_pts[0], goal_pts[0], ox, oy)
    path2 = astar(start_pts[1], goal_pts[1], ox, oy)
    path3 = astar(start_pts[2], goal_pts[2], ox, oy)
    path4 = astar(start_pts[3], goal_pts[3], ox, oy)
    window_size = 8

    path_list = []
    path_list.append(path1)
    path_list.append(path2)
    path_list.append(path3)
    path_list.append(path4)
    path_all = plot_path_update(path_list)
    path1 = path_all[0]
    path2 = path_all[1]
    path3 = path_all[2]
    path4 = path_all[3]
    path1 = make_8_step_path(path1, window_size)
    path2 = make_8_step_path(path2, window_size)
    path3 = make_8_step_path(path3, window_size)
    path4 = make_8_step_path(path4, window_size)

    m = len(path1)//window_size
    # print("m = ", m)
    # print(f'path1 = {len(path1)} \npath2 = {len(path2)} \npath3 = {len(path3)}')

    prev_path_list = []
    prev_path_list.append(path1)
    for i in range(m):
        p = (i-1)*window_size + window_size
        q = i*window_size + window_size
        # print('start index = ', p, ', end index = ', q)
        # path2 = reroute_window(path1[p:q], path2, p, q, ox, oy)
        path2 = reroute_window2(prev_path_list, path2, p, q, ox, oy)
        path_list = []
        path_list.append(path1)
        path_list.append(path2)
        path_list.append(path3)
        path_list.append(path4)
        path_all = plot_path_update(path_list)
        path1 = path_all[0]
        path2 = path_all[1]
        path3 = path_all[2]
        path4 = path_all[3]
        path1 = make_8_step_path(path1, window_size)
        path2 = make_8_step_path(path2, window_size)
        path3 = make_8_step_path(path3, window_size)
        path4 = make_8_step_path(path4, window_size)

        # path2 = make_8_step_path(path2, window_size)
    print('done finding path 2')
    prev_path_list.append(path2)
    for i in range(m):
        p = (i-1)*window_size + window_size
        q = i*window_size + window_size
        # print('start index = ', p, ', end index = ', q)
        # path2 = reroute_window(path1[p:q], path2, p, q, ox, oy)
        path3 = reroute_window2(prev_path_list, path3, p, q, ox, oy)
        path_list = []
        path_list.append(path1)
        path_list.append(path2)
        path_list.append(path3)
        path_list.append(path4)
        path_all = plot_path_update(path_list)
        path1 = path_all[0]
        path2 = path_all[1]
        path3 = path_all[2]
        path4 = path_all[3]
        path1 = make_8_step_path(path1, window_size)
        path2 = make_8_step_path(path2, window_size)
        path3 = make_8_step_path(path3, window_size)
        path4 = make_8_step_path(path4, window_size)

    print('done finding path 3')

    prev_path_list.append(path3)
    for i in range(m):
        p = (i-1)*window_size + window_size
        q = i*window_size + window_size
        # print('start index = ', p, ', end index = ', q)
        # path2 = reroute_window(path1[p:q], path2, p, q, ox, oy)
        path4 = reroute_window2(prev_path_list, path4, p, q, ox, oy)
        path_list = []
        path_list.append(path1)
        path_list.append(path2)
        path_list.append(path3)
        path_list.append(path4)
        path_all = plot_path_update(path_list)
        path1 = path_all[0]
        path2 = path_all[1]
        path3 = path_all[2]
        path4 = path_all[3]
        path1 = make_8_step_path(path1, window_size)
        path2 = make_8_step_path(path2, window_size)
        path3 = make_8_step_path(path3, window_size)
        path4 = make_8_step_path(path4, window_size)

    print('done finding path 4')

    path_list = []
    path_list.append(path1)
    path_list.append(path2)
    path_list.append(path3)
    path_list.append(path4)
    path_all = plot_path_update(path_list)

    # --------------------------------------- start of plotting -----------------------------------------------
    vis = 1
    if vis:
        for i in range(len(path_all[0])):
            plt.cla()
            # plt.plot(ox, oy, 'sk')
            show_loading_dock()
            draw_shelves()
            for start, goal in zip(start_pts, goal_pts):
                draw_endpoint(start, 'orange')
                draw_endpoint(goal, 'black')

            for path_n in path_all:
                draw_bot(path_n[i][0], path_n[i][1], "robot.png")
                # print(path_n[i][0], path_n[i][1],i, end=', ')
            # print('\n')
            plt.axis('equal')
            plt.xlim([-5, 50])
            plt.ylim([-5, 50])
            plt.title(
                f'First run, robots pick objects from bottom shelf, time = {i}')
            # plt.show(block=False)
            plt.pause(0.2)
    # plt.show()

    # new run for going to taking collected items from shelves to loading dock
    print("-------------------------\\-------------------")
    print("bringing items bacl to the loading dock")
    goal_pts = [(5, 25), (19, 25), (35, 25), (10, 23)]
    start_pts = [(35, 39), (38, 35), (8, 35), (22, 37)]

    ox, oy = [], []
    path_list = []
    ox, oy = make_obs(ox, oy)
    # store goal reaching time
    goal_times = []
    for i in range(len(start_pts)):
        # calculate shortest path
        path = astar(start_pts[i], goal_pts[i], ox, oy)
        timed_keys = time_a_star(path)
        # create a path lists for plotting
        path_list.append(path)
        path_all = plot_path_update(path_list)

    path1 = astar(start_pts[0], goal_pts[0], ox, oy)
    path2 = astar(start_pts[1], goal_pts[1], ox, oy)
    path3 = astar(start_pts[2], goal_pts[2], ox, oy)
    path4 = astar(start_pts[3], goal_pts[3], ox, oy)
    window_size = 8

    path_list = []
    path_list.append(path1)
    path_list.append(path2)
    path_list.append(path3)
    path_list.append(path4)
    path_all = plot_path_update(path_list)
    path1 = path_all[0]
    path2 = path_all[1]
    path3 = path_all[2]
    path4 = path_all[3]
    path1 = make_8_step_path(path1, window_size)
    path2 = make_8_step_path(path2, window_size)
    path3 = make_8_step_path(path3, window_size)
    path4 = make_8_step_path(path4, window_size)

    m = len(path1)//window_size
    # print("m = ", m)
    # print(f'path1 = {len(path1)} \npath2 = {len(path2)} \npath3 = {len(path3)}')

    prev_path_list = []
    prev_path_list.append(path1)
    for i in range(m):
        p = (i-1)*window_size + window_size
        q = i*window_size + window_size
        # print('start index = ', p, ', end index = ', q)
        # path2 = reroute_window(path1[p:q], path2, p, q, ox, oy)
        path2 = reroute_window2(prev_path_list, path2, p, q, ox, oy)
        path_list = []
        path_list.append(path1)
        path_list.append(path2)
        path_list.append(path3)
        path_list.append(path4)
        path_all = plot_path_update(path_list)
        path1 = path_all[0]
        path2 = path_all[1]
        path3 = path_all[2]
        path4 = path_all[3]
        path1 = make_8_step_path(path1, window_size)
        path2 = make_8_step_path(path2, window_size)
        path3 = make_8_step_path(path3, window_size)
        path4 = make_8_step_path(path4, window_size)

    m = len(path2)//window_size
    # print("m = ", m)
    # print(f'path1 = {len(path1)} \npath2 = {len(path2)} \npath3 = {len(path3)}')

    prev_path_list.append(path2)
    for i in range(m):
        p = (i-1)*window_size + window_size
        q = i*window_size + window_size
        # print('start index = ', p, ', end index = ', q)
        # path2 = reroute_window(path1[p:q], path2, p, q, ox, oy)
        path3 = reroute_window2(prev_path_list, path3, p, q, ox, oy)
        path_list = []
        path_list.append(path1)
        path_list.append(path2)
        path_list.append(path3)
        path_all = plot_path_update(path_list)
        path1 = path_all[0]
        path2 = path_all[1]
        path3 = path_all[2]
        path1 = make_8_step_path(path1, window_size)
        path2 = make_8_step_path(path2, window_size)
        path3 = make_8_step_path(path3, window_size)

    print('done finding path 3')

    prev_path_list.append(path3)
    for i in range(m):
        p = (i-1)*window_size + window_size
        q = i*window_size + window_size
        # print('start index = ', p, ', end index = ', q)
        # path2 = reroute_window(path1[p:q], path2, p, q, ox, oy)
        path4 = reroute_window2(prev_path_list, path4, p, q, ox, oy)
        path_list = []
        path_list.append(path1)
        path_list.append(path2)
        path_list.append(path3)
        path_list.append(path4)
        path_all = plot_path_update(path_list)
        path1 = path_all[0]
        path2 = path_all[1]
        path3 = path_all[2]
        path4 = path_all[3]
        path1 = make_8_step_path(path1, window_size)
        path2 = make_8_step_path(path2, window_size)
        path3 = make_8_step_path(path3, window_size)
        path4 = make_8_step_path(path4, window_size)

    path_list = []
    path_list.append(path1)
    path_list.append(path2)
    path_list.append(path3)
    path_list.append(path4)
    path_all = plot_path_update(path_list)

    # --------------------------------------- start of plotting -----------------------------------------------
    vis = 1
    if vis:
        for i in range(len(path_all[0])):
            plt.cla()
            # plt.plot(ox, oy, 'sk')
            show_loading_dock()
            draw_shelves()
            for start, goal in zip(start_pts, goal_pts):
                draw_endpoint(start, 'orange')
                draw_endpoint(goal, 'black')

            for path_n in path_all:
                draw_bot(path_n[i][0], path_n[i][1], "robot.png")
                # print(path_n[i][0], path_n[i][1],i, end=', ')
            # print('\n')
            plt.axis('equal')
            plt.xlim([-5, 50])
            plt.ylim([-5, 50])
            plt.title(
                f'First run, robots pick objects from top shelf, time = {i}')
            # plt.show(block=False)
            plt.pause(0.2)

    # new run for going from loading dock to collect items from bottom shelf
    print("-------------------------\\-------------------")
    print("second run - from the loading dock to the bottom shelf")
    start_pts = [(5, 25), (19, 25), (35, 25), (10, 23)]
    goal_pts = [(35, 11), (38, 14), (8, 15), (22, 13)]

    ox, oy = [], []
    path_list = []
    ox, oy = make_obs(ox, oy)
    # store goal reaching time
    goal_times = []
    for i in range(len(start_pts)):
        # calculate shortest path
        path = astar(start_pts[i], goal_pts[i], ox, oy)
        timed_keys = time_a_star(path)
        # create a path lists for plotting
        path_list.append(path)
        path_all = plot_path_update(path_list)

    path1 = astar(start_pts[0], goal_pts[0], ox, oy)
    path2 = astar(start_pts[1], goal_pts[1], ox, oy)
    path3 = astar(start_pts[2], goal_pts[2], ox, oy)
    path4 = astar(start_pts[3], goal_pts[3], ox, oy)
    window_size = 8

    path_list = []
    path_list.append(path1)
    path_list.append(path2)
    path_list.append(path3)
    path_list.append(path4)
    path_all = plot_path_update(path_list)
    path1 = path_all[0]
    path2 = path_all[1]
    path3 = path_all[2]
    path4 = path_all[3]
    path1 = make_8_step_path(path1, window_size)
    path2 = make_8_step_path(path2, window_size)
    path3 = make_8_step_path(path3, window_size)
    path4 = make_8_step_path(path4, window_size)

    m = len(path1)//window_size

    prev_path_list = []
    prev_path_list.append(path1)
    for i in range(m):
        p = (i-1)*window_size + window_size
        q = i*window_size + window_size
        # print('start index = ', p, ', end index = ', q)
        # path2 = reroute_window(path1[p:q], path2, p, q, ox, oy)
        path2 = reroute_window2(prev_path_list, path2, p, q, ox, oy)
        path_list = []
        path_list.append(path1)
        path_list.append(path2)
        path_list.append(path3)
        path_list.append(path4)
        path_all = plot_path_update(path_list)
        path1 = path_all[0]
        path2 = path_all[1]
        path3 = path_all[2]
        path4 = path_all[3]
        path1 = make_8_step_path(path1, window_size)
        path2 = make_8_step_path(path2, window_size)
        path3 = make_8_step_path(path3, window_size)
        path4 = make_8_step_path(path4, window_size)

    m = len(path2)//window_size

    prev_path_list.append(path2)
    for i in range(m):
        p = (i-1)*window_size + window_size
        q = i*window_size + window_size
        # print('start index = ', p, ', end index = ', q)
        # path2 = reroute_window(path1[p:q], path2, p, q, ox, oy)
        path3 = reroute_window2(prev_path_list, path3, p, q, ox, oy)
        path_list = []
        path_list.append(path1)
        path_list.append(path2)
        path_list.append(path3)
        path_all = plot_path_update(path_list)
        path1 = path_all[0]
        path2 = path_all[1]
        path3 = path_all[2]
        path1 = make_8_step_path(path1, window_size)
        path2 = make_8_step_path(path2, window_size)
        path3 = make_8_step_path(path3, window_size)

    prev_path_list.append(path3)
    for i in range(m):
        p = (i-1)*window_size + window_size
        q = i*window_size + window_size
        # print('start index = ', p, ', end index = ', q)
        # path2 = reroute_window(path1[p:q], path2, p, q, ox, oy)
        path4 = reroute_window2(prev_path_list, path4, p, q, ox, oy)
        path_list = []
        path_list.append(path1)
        path_list.append(path2)
        path_list.append(path3)
        path_list.append(path4)
        path_all = plot_path_update(path_list)
        path1 = path_all[0]
        path2 = path_all[1]
        path3 = path_all[2]
        path4 = path_all[3]
        path1 = make_8_step_path(path1, window_size)
        path2 = make_8_step_path(path2, window_size)
        path3 = make_8_step_path(path3, window_size)
        path4 = make_8_step_path(path4, window_size)

    path_list = []
    path_list.append(path1)
    path_list.append(path2)
    path_list.append(path3)
    path_list.append(path4)
    path_all = plot_path_update(path_list)

    # --------------------------------------- start of plotting -----------------------------------------------
    vis = 1
    if vis:
        for i in range(len(path_all[0])):
            plt.cla()
            # plt.plot(ox, oy, 'sk')
            show_loading_dock()
            draw_shelves()
            for start, goal in zip(start_pts, goal_pts):
                draw_endpoint(start, 'orange')
                draw_endpoint(goal, 'black')

            for path_n in path_all:
                draw_bot(path_n[i][0], path_n[i][1], "robot.png")
                # print(path_n[i][0], path_n[i][1],i, end=', ')
            # print('\n')
            plt.axis('equal')
            plt.xlim([-5, 50])
            plt.ylim([-5, 50])
            plt.title(
                f'First run, robots pick objects from bottom shelf, time = {i}')
            # plt.show(block=False)
            plt.pause(0.2)

    # new run for going from loading dock to collect items from bottom shelf
    print("-------------------------\\-------------------")
    print("second run - from the loading dock to the bottom shelf")
    goal_pts = [(5, 25), (19, 25), (35, 25), (10, 23)]
    start_pts = [(35, 11), (38, 14), (8, 16), (22, 12)]

    ox, oy = [], []
    path_list = []
    ox, oy = make_obs(ox, oy)
    # store goal reaching time
    goal_times = []
    for i in range(len(start_pts)):
        # calculate shortest path
        path = astar(start_pts[i], goal_pts[i], ox, oy)
        timed_keys = time_a_star(path)
        # create a path lists for plotting
        path_list.append(path)
        path_all = plot_path_update(path_list)

    path1 = astar(start_pts[0], goal_pts[0], ox, oy)
    path2 = astar(start_pts[1], goal_pts[1], ox, oy)
    path3 = astar(start_pts[2], goal_pts[2], ox, oy)
    path4 = astar(start_pts[3], goal_pts[3], ox, oy)
    window_size = 8

    path_list = []
    path_list.append(path1)
    path_list.append(path2)
    path_list.append(path3)
    path_list.append(path4)
    path_all = plot_path_update(path_list)
    path1 = path_all[0]
    path2 = path_all[1]
    path3 = path_all[2]
    path4 = path_all[3]
    path1 = make_8_step_path(path1, window_size)
    path2 = make_8_step_path(path2, window_size)
    path3 = make_8_step_path(path3, window_size)
    path4 = make_8_step_path(path4, window_size)

    m = len(path1)//window_size

    prev_path_list = []
    prev_path_list.append(path1)
    for i in range(m):
        p = (i-1)*window_size + window_size
        q = i*window_size + window_size
        # print('start index = ', p, ', end index = ', q)
        # path2 = reroute_window(path1[p:q], path2, p, q, ox, oy)
        path2 = reroute_window2(prev_path_list, path2, p, q, ox, oy)
        path_list = []
        path_list.append(path1)
        path_list.append(path2)
        path_list.append(path3)
        path_list.append(path4)
        path_all = plot_path_update(path_list)
        path1 = path_all[0]
        path2 = path_all[1]
        path3 = path_all[2]
        path4 = path_all[3]
        path1 = make_8_step_path(path1, window_size)
        path2 = make_8_step_path(path2, window_size)
        path3 = make_8_step_path(path3, window_size)
        path4 = make_8_step_path(path4, window_size)

    m = len(path2)//window_size

    prev_path_list.append(path2)
    for i in range(m):
        p = (i-1)*window_size + window_size
        q = i*window_size + window_size
        # print('start index = ', p, ', end index = ', q)
        # path2 = reroute_window(path1[p:q], path2, p, q, ox, oy)
        path3 = reroute_window2(prev_path_list, path3, p, q, ox, oy)
        path_list = []
        path_list.append(path1)
        path_list.append(path2)
        path_list.append(path3)
        path_all = plot_path_update(path_list)
        path1 = path_all[0]
        path2 = path_all[1]
        path3 = path_all[2]
        path1 = make_8_step_path(path1, window_size)
        path2 = make_8_step_path(path2, window_size)
        path3 = make_8_step_path(path3, window_size)

    prev_path_list.append(path3)
    for i in range(m):
        p = (i-1)*window_size + window_size
        q = i*window_size + window_size
        # print('start index = ', p, ', end index = ', q)
        # path2 = reroute_window(path1[p:q], path2, p, q, ox, oy)
        path4 = reroute_window2(prev_path_list, path4, p, q, ox, oy)
        path_list = []
        path_list.append(path1)
        path_list.append(path2)
        path_list.append(path3)
        path_list.append(path4)
        path_all = plot_path_update(path_list)
        path1 = path_all[0]
        path2 = path_all[1]
        path3 = path_all[2]
        path4 = path_all[3]
        path1 = make_8_step_path(path1, window_size)
        path2 = make_8_step_path(path2, window_size)
        path3 = make_8_step_path(path3, window_size)
        path4 = make_8_step_path(path4, window_size)

    path_list = []
    path_list.append(path1)
    path_list.append(path2)
    path_list.append(path3)
    path_list.append(path4)
    path_all = plot_path_update(path_list)

    # --------------------------------------- start of plotting -----------------------------------------------
    vis = 1
    if vis:
        for i in range(len(path_all[0])):
            plt.cla()
            # plt.plot(ox, oy, 'sk')
            show_loading_dock()
            draw_shelves()
            for start, goal in zip(start_pts, goal_pts):
                draw_endpoint(start, 'orange')
                draw_endpoint(goal, 'black')

            for path_n in path_all:
                draw_bot(path_n[i][0], path_n[i][1], "robot.png")
                # print(path_n[i][0], path_n[i][1],i, end=', ')
            # print('\n')
            plt.axis('equal')
            plt.xlim([-5, 50])
            plt.ylim([-5, 50])
            plt.title(
                f'First run, robots pick objects from bottom shelf, time = {i}')
            # plt.show(block=False)
            plt.pause(0.2)
    x = 4
    # eoc


if __name__ == "__main__":
    main()
