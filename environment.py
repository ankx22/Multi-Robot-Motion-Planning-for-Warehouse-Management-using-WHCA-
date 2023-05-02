import matplotlib.pyplot as plt
import numpy as np
import math


def create_shelf(left_top_corner, width, height):
    top_left_x = left_top_corner[0]
    top_left_y = left_top_corner[1]
    shelve_x, shelve_y = [], []
    for i in range(top_left_x, top_left_x + width + 1):
        shelve_x.append(i)
        shelve_y.append(top_left_y)
    for i in range(top_left_x, top_left_x + width + 1):
        shelve_x.append(i)
        shelve_y.append(top_left_y-height)
    for i in range(top_left_y-height, top_left_y + 1):
        shelve_x.append(top_left_x)
        shelve_y.append(i)
    for i in range(top_left_y-height, top_left_y + 1):
        shelve_x.append(top_left_x + width)
        shelve_y.append(i)
    return shelve_x, shelve_y


def create_map(maxx, maxy):
    ox, oy = [], []
    # external boundary
    for i in range(maxx):
        ox.append(i)
        oy.append(0)
    for i in range(maxx):
        ox.append(i)
        oy.append(maxy-1)
    for i in range(maxy):
        ox.append(0)
        oy.append(i)
    for i in range(maxy):
        ox.append(maxx-1)
        oy.append(i)

    VT1 = (7, 14)
    Sh_w = 3
    Sh_h = 8

    # vertical shelves placement
    num_rows = 2
    num_shelves = 4  # shelves in one row
    for j in range(num_rows):
        for i in range(num_shelves):
            # top_left = (VT1[0] + i*50, VT1[1] + j*150)
            top_left = (VT1[0] + i*8, VT1[1] + j*25)
            sh_x, sh_y = create_shelf(top_left, Sh_w, Sh_h)
            for ix, iy in zip(sh_x, sh_y):
                ox.append(ix)
                oy.append(iy)

    # horizontal shelve placement
    # HT1 = (40,160)
    # Sh_w = 80
    # Sh_h = 20

    HT1 = (7, 26)
    Sh_w = 13
    Sh_h = 3

    # vertical shelves placement
    num_rows = 1
    num_shelves = 2  # shelves in one row
    for j in range(num_rows):
        for i in range(num_shelves):
            # top_left = (HT1[0] + i*140, HT1[1] + j*150)
            top_left = (HT1[0] + i*23, HT1[1] + j*23)
            sh_x, sh_y = create_shelf(top_left, Sh_w, Sh_h)
            for ix, iy in zip(sh_x, sh_y):
                ox.append(ix)
                oy.append(iy)

    return ox, oy
