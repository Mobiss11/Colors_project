import cv2
import numpy as np


def get_image_colors(image):
    """ We get the colors from the incoming iso image """
    title_image = cv2.imread(str(image))

    matrix_image = cv2.resize(title_image, (title_image.shape[1] // 12, title_image.shape[0] // 12))

    height_image = np.size(matrix_image, 0)
    width_image = np.size(matrix_image, 1)

    colors_input = []
    colors_output = []

    for first_coordinate in range(1, width_image):
        for second_coordinate in range(1, height_image):
            (b, g, r) = matrix_image[second_coordinate, first_coordinate]
            color_format = str((r, g, b))
            colors_input.append(color_format)

    for color in colors_input:
        if color not in colors_output:
            colors_output.append(color)

    return colors_output
