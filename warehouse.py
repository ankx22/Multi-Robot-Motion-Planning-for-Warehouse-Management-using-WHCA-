import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image


def draw_shelves():
    zoom = 0.4
    # Load the image and resize it
    img = Image.open('shelf.png')

    # Create an OffsetImage object using the image
    img_object = OffsetImage(img, zoom=zoom)

    # Create an AnnotationBbox object to display the image at the given coordinates
    x1 = 5
    y1 = 15.5
    ab1 = AnnotationBbox(img_object, (x1, y1), frameon=False)
    plt.gca().add_artist(ab1)

    x2 = 15
    y2 = 15.5
    ab2 = AnnotationBbox(img_object, (x2, y2), frameon=False)
    plt.gca().add_artist(ab2)

    x3 = 25
    y3 = 15.5
    ab3 = AnnotationBbox(img_object, (x3, y3), frameon=False)
    plt.gca().add_artist(ab3)

    x4 = 35
    y4 = 15.5
    ab4 = AnnotationBbox(img_object, (x4, y4), frameon=False)
    plt.gca().add_artist(ab4)
    # top shelves
    x1 = 5
    y1 = 35
    ab1 = AnnotationBbox(img_object, (x1, y1), frameon=False)
    plt.gca().add_artist(ab1)

    x2 = 15
    y2 = 35
    ab2 = AnnotationBbox(img_object, (x2, y2), frameon=False)
    plt.gca().add_artist(ab2)

    x3 = 25
    y3 = 35
    ab3 = AnnotationBbox(img_object, (x3, y3), frameon=False)
    plt.gca().add_artist(ab3)

    x4 = 35
    y4 = 35
    ab4 = AnnotationBbox(img_object, (x4, y4), frameon=False)
    plt.gca().add_artist(ab4)


def make_obs(ox, oy):
    # uncomment below code block for original display of windowed A-star where path1 and path2 intersect without local planning using a window
    '''
    for i in range(15,21):
            ox.append(i)
            oy.append(12)

    for i in range(15,22):
            ox.append(i)
            oy.append(19)

    for i in range(12,19):
            oy.append(i)
            ox.append(15)

    for i in range(12,19):
            oy.append(i)
            ox.append(21)
    '''
    for i in range(3, 8):
        ox.append(i)
        oy.append(12)

    for i in range(3, 8):
        ox.append(i)
        oy.append(19)

    for i in range(12, 20):
        oy.append(i)
        ox.append(3)

    for i in range(12, 20):
        oy.append(i)
        ox.append(7)

    for i in range(13, 18):
        ox.append(i)
        oy.append(12)

    for i in range(13, 18):
        ox.append(i)
        oy.append(19)

    for i in range(12, 20):
        oy.append(i)
        ox.append(13)

    for i in range(12, 20):
        oy.append(i)
        ox.append(17)

    for i in range(23, 28):
        ox.append(i)
        oy.append(12)

    for i in range(23, 28):
        ox.append(i)
        oy.append(19)

    for i in range(12, 20):
        oy.append(i)
        ox.append(23)

    for i in range(12, 20):
        oy.append(i)
        ox.append(27)

    for i in range(33, 38):
        ox.append(i)
        oy.append(12)

    for i in range(33, 38):
        ox.append(i)
        oy.append(19)

    for i in range(12, 20):
        oy.append(i)
        ox.append(33)

    for i in range(12, 20):
        oy.append(i)
        ox.append(37)

    # Obstacles are 2nd row of shelves
    for i in range(3, 8):
        ox.append(i)
        oy.append(32)

    for i in range(3, 8):
        ox.append(i)
        oy.append(38)

    for i in range(32, 39):
        oy.append(i)
        ox.append(3)

    for i in range(32, 39):
        oy.append(i)
        ox.append(7)

    for i in range(13, 18):
        ox.append(i)
        oy.append(32)

    for i in range(13, 18):
        ox.append(i)
        oy.append(38)

    for i in range(32, 39):
        oy.append(i)
        ox.append(13)

    for i in range(32, 39):
        oy.append(i)
        ox.append(17)

    for i in range(23, 28):
        ox.append(i)
        oy.append(32)

    for i in range(23, 28):
        ox.append(i)
        oy.append(38)

    for i in range(32, 39):
        oy.append(i)
        ox.append(23)

    for i in range(32, 39):
        oy.append(i)
        ox.append(27)

    for i in range(33, 38):
        ox.append(i)
        oy.append(32)

    for i in range(33, 38):
        ox.append(i)
        oy.append(38)

    for i in range(32, 39):
        oy.append(i)
        ox.append(33)

    for i in range(32, 39):
        oy.append(i)
        ox.append(37)

    return ox, oy


def show_loading_dock():
    ox, oy = [], []
    for i in range(0, 40):
        ox.append(i)
        oy.append(23)

    for i in range(23, 26):
        oy.append(i)
        ox.append(0)

    for i in range(0, 40):
        ox.append(i)
        oy.append(26)

    for i in range(23, 27):
        oy.append(i)
        ox.append(40)
    plt.plot(ox, oy, 'sg')

    # ox1 = [5, 40, 40, 5, 5]
    # oy1 = [23, 23, 27, 27, 23]

    # plt.plot(ox1, oy1, 'g')

    # ox2 = [6, 39, 39, 6, 6]
    # oy2 = [24, 24, 26, 26, 24]

    # plt.plot(ox2, oy2, 'g')
