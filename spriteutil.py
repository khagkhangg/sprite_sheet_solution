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


class Sprite():
    def __init__(self, label, x1, y1, x2, y2):
        """
        All arguments (except self) MUST be strictly positive integers
        """

        # Check validation
        if not self.is_valid_arguments(label, x1, y1, x2, y2):
            raise ValueError("Invalid coordinates")

        # These properties are read-only
        self._label = label
        self._top_left = (x1, y1)
        self._bottom_right = (x2, y2)

        # These are not read-only
        self.width = x2 - x1 + 1
        self.height = y2 - y1 + 1

    @property
    def label(self):
        return self._label

    @property
    def top_left(self):
        return self._top_left

    @property
    def bottom_right(self):
        return self._bottom_right

    def is_valid_arguments(self, label, x1, y1, x2, y2):
        """
        Check validation of passed arguments

        All arguments MUST be non-negative Interger and
        x2 and y2 MUST be equal or greater respectively than x1 and y1

        Return True by default and False when requirement is not met
        """

        for element in [label, x1, y1, x2, y2]:
            if type(element) is not int or element < 0 or x2 < x1 or y2 < y1:
                return False
        return True
