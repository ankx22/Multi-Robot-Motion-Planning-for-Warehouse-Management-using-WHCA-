import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image


class C:
    PI = math.pi
    RB = 0.25
    RF = 0.25
    W = 0.5


def draw_bot(x, y, image_path, zoom=0.025):
    # Load the image and resize it
    img = Image.open(image_path)

    # Create an OffsetImage object using the image
    img_object = OffsetImage(img, zoom=zoom)

    # Create an AnnotationBbox object to display the image at the given coordinates
    ab = AnnotationBbox(img_object, (x, y), frameon=False)
    plt.gca().add_artist(ab)


def draw_endpoint(point, color='black'):
    end = np.array([[C.RB+0.1, -C.RB-0.1, -C.RF-0.1, C.RF+0.1, C.RB+0.1],
                    [C.W/2+0.1, C.W/2+0.1, -C.W/2-0.1, -C.W/2-0.1, C.W/2+0.1]])
    end += np.array([[point[0]], [point[1]]])
    plt.plot(end[0, :], end[1, :], color)
