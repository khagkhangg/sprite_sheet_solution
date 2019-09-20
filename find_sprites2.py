from find_most_common_color import find_most_common_color
from PIL import Image
from numpy import amax, where, array, zeros, append
from pprint import pprint
import timeit


class Sprite():
    def __init__(self, label, x1, y1, x2, y2):
        """ All arguments (except self) MUST be strictly positive integers
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
        """ Check validation of passed arguments

        All arguments MUST be non-negative Interger and
        x2 and y2 MUST be equal or greater respectively than x1 and y1

        Return True by default and False when requirement is not met
        """

        for element in [label, x1, y1, x2, y2]:
            if type(element) is not int or element < 0 or x2 < x1 or y2 < y1:
                return False
        return True


class Pixel():
    def __init__(self, row, column, is_background_pixel):
        # Axe x
        self.column = column
        # Axe y
        self.row = row
        # Boolean value, True if it is a background pixel
        self.is_background_pixel = is_background_pixel
        # Positive natural number
        self.label = 0

    def __repr__(self):
        return str(self.label)


def find_sprites(image=None, background_color=None):
    """ Find sprites

    @image: MUST be an Image object
    @background_color: optinal, whether tuple (RGB/ RGBA) or int (grayscale)
    """

    def find_sprites_corners(sprite, label_map, numpy_array):
        columns = set()
        rows = set()
        for row_index, row in enumerate(numpy_array):
            for column_index, column in enumerate(row):
                current_pixel = label_map[row_index][column_index]
                if current_pixel.label == sprite:
                    columns.add(current_pixel.column)
                    rows.add(current_pixel.row)
        return min(columns), min(rows), max(columns), max(rows)

    def collect_sprites(exist_sprites_label, label_map, numpy_array):
        """ Return A dictionary with key:the label of a sprite and value:it's Sprite object
        """
        sprites = {}
        for sprite in exist_sprites_label:
            top_left_column, top_left_row, bottom_right_column, bottom_right_row = find_sprites_corners(sprite, label_map, numpy_array)
            sprites[sprite] = Sprite(sprite, top_left_column, top_left_row, bottom_right_column, bottom_right_row)

        return sprites

    def search_exist_sprites_label(pixels_to_sprites):
        """ Return a set of exist sprite's label inside the map
        """
        exist_sprites = set()
        for key in pixels_to_sprites:
            exist_sprites.add(pixels_to_sprites[key])
        return exist_sprites

    def unify_sprites(pixels_to_sprites, unified_matrix, numpy_array):
        """ Unify all pixels that are in a same sprite

        Return a 2D-array map of sprites
        """
        for row_index, row in enumerate(numpy_array):
            for column_index, column in enumerate(row):
                current_pixel = pixels_matrix[row_index][column_index]
                current_label = current_pixel.label
                # Ignore background pixels
                if current_label == 0 or current_label not in pixels_to_sprites:
                    continue
                current_pixel.label = pixels_to_sprites[current_label]
        return unified_matrix

    def analyze_connected_sprites(connected_sprites):
        """ Find all pixels that are connected (belong to a same sprite)

        Return a dict:
            key: pixel'label
            value: sprite's label that key belong to
        """
        pixels_to_sprites = {}
        for key in list(connected_sprites.keys()):
            if key not in connected_sprites or len(connected_sprites[key]) == 1:
                continue
            in_progress = True
            old_length = len(connected_sprites[key])
            while in_progress:
                for value in connected_sprites[key]:
                    if value not in connected_sprites:
                        continue
                    connected_sprites[key] = connected_sprites[key] | connected_sprites[value]
                    if value in connected_sprites and value != key:
                        del connected_sprites[value]

                if old_length == len(connected_sprites[key]):
                    in_progress = False
                else:
                    old_length = len(connected_sprites[key])

        for key in connected_sprites:
            for value in connected_sprites[key]:
                pixels_to_sprites[value] = key
        return pixels_to_sprites

    def is_new_sprite(current_row, current_column, pixels_matrix, background_color):
        """ Return False if there is a non-background pixel adjacent to current pixel
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
                if current_pixel.label != 0 and current_pixel.label != neighbor_pixel.label:
                    connected_sprites.setdefault(current_pixel.label, set()).add(neighbor_pixel.label)
                else:
                    pixels_matrix[current_row][current_column].label = neighbor_pixel.label
                    is_new_sprite = False

        return is_new_sprite

    def is_ignored_pixel(current_pixel, numpy_array):
        """ Check if that pixel is considered background pixel

        Return False by default
        """
        if (background_color == (0,0,0,0) and current_pixel[-1] == 0) or (current_pixel == array(background_color)).all() or (image.mode == "L" and current_pixel == background_color):
            return True
        return False

    def analyze_numpy_array(background_color):
        """ Convert image to numpy array then analyze each pixel

        @background_color: RGBA or RGB or grayscale formats

        Return Maps of pixels under format matrix and numpy array (multi-dimensional)
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
                    connected_sprites.setdefault(new_label, set()).add(new_label)


        return pixels_matrix, numpy_array

    def is_valid_background_color():
        """ Check if arg @background_color is valid

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
    # Store all connected sprites that can be unified latter
    connected_sprites = {}
    # List of pixels label exist inside the map
    sprites_label = [0]
    # Maps of pixels under format matrix and numpy array
    pixels_matrix, numpy_array = analyze_numpy_array(background_color)
    # Dict of pixels'label corresponding to sprite's label
    pixels_to_sprites = analyze_connected_sprites(connected_sprites)
    # Map of sprites under format 2D-matrix
    label_map = unify_sprites(pixels_to_sprites, pixels_matrix, numpy_array)
    # Set of sprite-label that exist inside the map
    exist_sprites_label = search_exist_sprites_label(pixels_to_sprites)
    # A dictionary with key:the label of a sprite and value:it's Sprite object
    sprites = collect_sprites(exist_sprites_label, label_map, numpy_array)
    return (sprites, label_map)

image = Image.open("optimized_sprite_sheet.png")
sprites, label_map = find_sprites(image)

# for label, sprite in sprites.items():
#     print(f"Sprite ({label}): [{sprite.top_left}, {sprite.bottom_right}] {sprite.width}x{sprite.height}")
a = timeit.timeit(stmt=lambda: find_sprites(image), number=1)
print(a)
