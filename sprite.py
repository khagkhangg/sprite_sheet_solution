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


# sprite = Sprite(1, 12, 23, 145, 208)
# print(sprite.label)
# print(sprite.top_left)
# print(sprite.bottom_right)
# print(sprite.width)
# print(sprite.height)
#
# sprite = Sprite(-1, 0, 0, 0)
# sprite = Sprite("Hello", 0, 0, 0)
# sprite = Sprite(1, 0, 0, 0)
