import matplotlib.pyplot as plt
from draw import *
from astar import *

ox, oy = [], []
path_all = []
path1 = [(7, 4), (6, 4), (5, 4), (5, 3)]
path2 = [(4, 4), (5, 4), (6, 4), (7, 4)]


class path:
    def __init__():
        path.time = []
        path.type = None
        path.line = None


def intersection(line1, line2):
    xy1 = []
    xy2 = []
    for pt in line1:
        xy1.append((pt[0], pt[1]))
    for pt in line2:
        xy2.append((pt[0], pt[1]))

    print('xy1 = ', xy1)
    print('xy2 = ', xy2)
    inter = list(set(xy1) & set(xy2))
    return inter


def check_intersection(path1, path2):
    time_keys = time_a_star(path1)
    print(f'data type = {time_keys}')
    print(f'data type = {type(time_keys)}')
    line2 = []
    line1 = []
    for i in range(len(path2)-1):
        print(path2[i][0], path2[i][1], i)
        if (path2[i][0], path2[i][1], i+1) in time_keys and (path2[i+1][0], path2[i+1][1], i) in time_keys:
            # for path1
            m = i-1
            n = i+2
            # for path1
            p = i
            q = i+2
            print(f'm = {m}, n = {n}, p = {p}, q = {q}')
            print('intersection at ', path2[i][0], path2[i][1],
                  i+1, ' and ', path2[i+1][0], path2[i+1][1], i)
            line2.append((path2[i][0], path2[i][1], i))
            line2.append((path2[i+1][0], path2[i+1][1], i+1))
            line1.append((path1[i+1][0], path1[i+1][1], i+1))

            if (path2[i][0] == path2[i+1][0]):
                linetype = 'x'
                x = path2[i][0]
            elif (path2[i][1] == path2[i+1][1]):
                linetype = 'y'
                y = path2[i][1]

            if linetype == 'x':
                while (m >= 0 and path2[m][0] == x):
                    line2.insert(0, (path2[m][0], path2[m][1], m))
                    m = m-1
                while (n < len(path2) and path2[n][0] == x):
                    line2.append((path2[n][0], path2[n][1], n))
                    n = n+1

                while (p >= 0 and path1[p][0] == x):
                    line1.insert(0, (path1[p][0], path1[p][1], p))
                    p = p-1
                while (q < len(path1) and path1[q][0] == x):
                    line1.append((path1[q][0], path1[q][1], q))
                    q = q+1

            if linetype == 'y':
                while (m >= 0 and path2[m][1] == y):
                    line2.insert(0, (path2[m][0], path2[m][1], m))
                    m = m-1
                while (n < len(path2) and path2[n][1] == y):
                    line2.append((path2[n][0], path2[n][1], n))
                    n = n+1

                while (p >= 0 and path1[p][1] == y):
                    line1.insert(0, (path1[p][0], path1[p][1], p))
                    p = p-1
                while (q < len(path1) and path1[q][1] == y):
                    line1.append((path1[q][0], path1[q][1], q))
                    q = q+1

            print(
                f'intersection was of type {linetype} and \nline2 = {line2}\nline1 = {line1}')
            inter = intersection(line1, line2)
            for t in range(len(inter)):
                path2.insert(i, path2[i-1])

        elif (path2[i][0], path2[i][1], i) in time_keys:
            intersection_length = 1
    return path2


path2 = check_intersection(path1, path2)
path_all.append(path1)
path_all.append(path2)


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


path_all = plot_path_update(path_all)
for i in range(len(path_all)):
    print(f'path{i} = {path_all[i]}')


start_pts, goal_pts = [], []
start_pts.append(path_all[0][0])
start_pts.append(path_all[1][0])
goal_pts.append(path_all[0][-1])
goal_pts.append(path_all[1][-1])

vis = 1
if vis:
    for i in range(len(path_all[0])):
        plt.cla()
        plt.plot(ox, oy, 'sk')
        for start, goal in zip(start_pts, goal_pts):
            # draw_endpoint(start, 'orange')
            draw_endpoint(goal, 'grey')

        for path_n in path_all:
            draw_bot(path_n[i][0], path_n[i][1])
            pathx = []
            pathy = []
            for point in path_n:
                pathx.append(point[0])
                pathy.append(point[1])
            plt.plot(pathx, pathy)
        plt.axis('equal')
        plt.xlim([2, 10])
        plt.ylim([0, 5])

        plt.show(block=False)
        plt.pause(1)
