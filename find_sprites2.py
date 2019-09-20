from find_most_common_color import find_most_common_color
from PIL import Image
from numpy import amax, where, array, zeros
from pprint import pprint


class Pixel():
    def __init__(self, row, column, is_background_pixel):
        self.row = row
        self.column = column
        self.is_background_pixel = is_background_pixel
        self.label = 0

    def __repr__(self):
        return str(self.label)


def find_sprites(image=None, background_color=None):
    """Find sprites

    @image: MUST be an Image object
    @background_color: optinal, whether tuple (RGB/ RGBA) or int (grayscale)
    """

    def is_new_sprite(current_row, current_column, pixels_matrix, background_color):
        """Return False if there is a non-background pixel adjacent to current pixel
        Ignores background pixels.
        """
        neighbor_coordinates = [(-1, -1), (-1, 0), (-1, 1), (0, -1)]
        current_pixel = pixels_matrix[current_row][current_column]
        is_new_sprite = True

        # Ignore background pixels
        if current_pixel.is_background_pixel:
            return False

        # Check 4 neighbor of current pixels
        for coordinate in neighbor_coordinates:
            neighbor_row = current_row + coordinate[0]
            neighbor_column = current_column + coordinate[1]
            if 0 <= neighbor_row < image_height and 0 <= neighbor_column < image_width:
                neighbor_pixel = pixels_matrix[neighbor_row][neighbor_column]
                if neighbor_pixel.label == 0:
                    continue
                
                else:
                    pixels_matrix[current_row][current_column].label = neighbor_pixel.label
                    is_new_sprite = False
        return is_new_sprite

    def is_ignored_pixel(current_pixel, numpy_array):
        if (background_color == 0 and current_pixel[-1] == 0) or (current_pixel == array(background_color)).all() or (image.mode == "L" and current_pixel == background_color):
            return True
        return False

    def analyze_numpy_array(background_color):
        """Convert image to numpy array then analyze each pixel

        @background_color: RGBA or RGB or grayscale formats
        """

        numpy_array = array(image)
        pixels_matrix = zeros(numpy_array.shape, dtype=int).tolist()

        for row_index, row in enumerate(numpy_array):
            for column_index, column in enumerate(row):
                current_pixel = numpy_array[row_index, column_index]
                pixels_matrix[row_index][column_index] = Pixel(row_index, column_index, is_ignored_pixel(current_pixel, numpy_array))

        for row_index, row in enumerate(numpy_array):
            for column_index, column in enumerate(row):
                if is_new_sprite(row_index, column_index, pixels_matrix, background_color):
                    new_label = sprites_label[-1] + 1
                    pixels_matrix[row_index][column_index].label = new_label
                    sprites_label.append(new_label)

        pprint(pixels_matrix, width=120)

    def is_valid_background_color():
        """Check if arg background_color is valid

        Return True by default
        """
        # Not int or tuple
        if type(background_color) not in (int, tuple):
            return False
        # Invalid grayscale format
        if type(background_color) == int:
            if not 255 >= background_color >= 0 or image.mode != "L":
                return False
        # Invalid RGB/ RGBA format
        if type(background_color) == tuple:
            if len(background_color) not in (3,4) or image.mode == "L":
                return False
            for element in background_color:
                if type(element) != int or not 255 >= element >= 0:
                    return False
        return True

    if background_color:
        pass
    elif image.mode == "RGBA":
        background_color = (0,0,0,0)
    else:
        background_color = find_most_common_color(image)

    # Check validation of arg background_color
    if not is_valid_background_color() or not image:
        print("Invalid arguments! Please try again!")
        return

    image_width, image_height = image.size
    # List of sprites label, start with value 0 which
    sprites_label = [0]
    analyze_numpy_array(background_color)


image = Image.open("metal_slug_single_sprite.png")
find_sprites(image)
