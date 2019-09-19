from PIL import Image
from numpy import amax, where


def find_most_common_color(image):
    """
    Find most used color in an Image object

    @arg: image: MUST be an Image object

    Return most used color in the image
    Format of the return value is same as image's mode
    """

    try:
        # List of color used and its occurence
        colors = image.getcolors(image.size[0]*image.size[1])
        # List of color occurrence
        occurrences = [color[0] for color in colors]
        # Index of the most most common color
        most_common_color_index = where(occurrences == amax(occurrences))[0][0]
        # Return most common color
        most_common_color = colors[most_common_color_index][1]
        return most_common_color
    except Exception:
        print("Your Image object is invalid! Please try another!")
