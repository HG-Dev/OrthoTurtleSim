''' Data classes that help to support smooth calculations in a 2D world '''

from math import sqrt
from enum import IntEnum
from dataclasses import dataclass
from collections import OrderedDict

def normalize(number):
    """ Clamps a number to be -1, 0, or 1. """
    if number == 0:
        return int(number)
    return int(number / abs(number))

@dataclass
class Coord:
    '''Class for keeping track of coordinates and running calculations between them.'''
    x: int = 0
    y: int = 0

    @classmethod
    def from_dict(cls, init_dict: dict):
        """
        Creates a Coord class using values taken from a dict
        """
        xyz_vals = [
            init_dict.get("x") or 0,
            init_dict.get("y") or 0
        ]
        return cls(*xyz_vals)

    def __add__(self, other):
        """ Addition operator function """
        return Coord(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other):
        """ Subtraction operator function """
        return Coord(x=self.x - other.x, y=self.y - other.y)

    def __radd__(self, other):
        """ Reverse add for non-Coord numbers """
        if other == 0:
            return self
        return self.__add__(other)

    def as_ordered_dict(self):
        """
        Returns sorted fields in the form of an OrderedDict
        dataclasses' "asdict" method could be used as an alternative
        to __dict__, but rumor has it pegged as a slug.
        """
        return OrderedDict(
            sorted(self.__dict__.items(), key=lambda keyval: abs(keyval[1]), reverse=True)
        )

    @property
    def sorted_ortho_normals(self):
        """
        Returns a list of orthographic normal Coords
        sorted by which axis is biggest
        """
        return [Coord.from_dict({key: normalize(val)}) for key, val in self.as_ordered_dict().items()]

    @property
    def max_axis(self):
        """
        Returns tuple with the biggest axis and its value
        """
        axis = None
        val = None
        for axis, val in self.as_ordered_dict().items():
            break
        return (axis, val)

    @property
    def max_ortho_normal(self):
        """
        Returns an orthographic normal (points in one cardinal direction,
        plus up and down) depending on which axis is biggest
        """
        axis = None
        val = None
        for axis, val in self.as_ordered_dict().items():
            break
        init_dict = {axis: normalize(val)}
        return Coord.from_dict(init_dict)

    @property
    def just_x(self):
        """ Returns self with zero for y """
        return Coord(self.x, 0)

    @property
    def just_y(self):
        """ Returns self with zero for x """
        return Coord(0, self.y)

    def dist_to(self, other):
        """ Returns the precise distance from this point to another """
        return Coord.dist_between(self, other)

    def is_on_line(self, point_a, point_b):
        """
        Returns True or False depending on whether this coordinate
        can be found on a line drawn between coordinates A and B.
        """
        #if all point form vertical line
        if point_a.x == point_b.x == self.x:
            return abs(point_a.y) < abs(self.y) < abs(point_b.y)
        #if all points form horizontal line
        if point_a.y == point_b.y == self.y:
            return abs(point_a.x) < abs(self.x) < abs(point_b.x)
        vector_line = point_a - point_b
        vector_self = self - point_b
        return (
            #Confirm linearity (cross product of a-b and c-b should be zero)
            Coord.cross_product(vector_line, vector_self) == 0
            #Use dot product to confirm self is between a and b
            #Dot product will be bigger than distance if left of a,
            #and negative if right of b
            and 0 <= Coord.dot_product(vector_line, vector_self) <= Coord.dist_between_squared(point_a, point_b)
        )
    
    @staticmethod
    def dist_between_squared(point_a, point_b):
        """ Returns the squared distance from point a to point b """
        return ((point_a.x - point_b.x) ** 2) + ((point_a.y - point_b.y) ** 2)

    @staticmethod
    def dist_between(point_a, point_b):
        """ Returns the precise distance from point a to point b """
        return sqrt(Coord.dist_between_squared(point_a, point_b))

    @staticmethod
    def dot_product(point_a, point_b):
        """ Returns the dot product of point a and point b as vectors """
        return (point_a.x * point_b.x) + (point_a.y * point_b.y)

    @staticmethod
    def cross_product(point_a, point_b):
        """
        Returns the cross product of (area of parallelogram between)
        point a and point b as vectors
        """
        return (point_a.x * point_b.y) - (point_b.x * point_a.y)

class HeadingType(IntEnum):
    """ Enumerator class used to identify which way an object faces or moves """
    EAST = 1
    WEST = 2
    NORTH = 3
    SOUTH = 4
    #Moving only
    DIR_UP = 5
    DIR_DOWN = 6

#types of pathing algorithms: true_vector, least_turns, lawnmower

@dataclass
class Heading():
    index: HeadingType = HeadingType.EAST

    @classmethod
    def from_vector(cls, motion_vector: Coord):
        """
        Converts a coordinate vector into a heading based on
        whatever axis has the largest value where ties are settled
        up-down -> forward-back -> left-right
        """
        #TODO consider heading
        #sorted_axis_keyvals = motion_vector.as_ordered_dict()
        axis, val = motion_vector.max_axis
        index = 1
        if axis == "y":
            index = 3
        elif axis == "z":
            index = 5
        
        if val < 0:
            index = index + 2

        return cls(index)

    @staticmethod
    def index_to_coord(index: int):
        """ Converts a heading index to a normal vector """
        x = index % 2
        y = (index % 2) - 1
        if 2 <= index <= 3:
            x = x * -1
            y = y * -1
        elif index >= 5:
            x = 0
            y = 0
        return Coord(x, y)

    @property
    def vector(self):
        """
        Returns a normal vector depending on the current set index.
        """
        return Heading.index_to_coord(self.index)

def simpletest():
    """
    Simple test used for feature development
    面倒くさいと思って色々考えたけど、ドット積は強いですね…
    """
    origin = Coord()
    coord_a = Coord(0,1)
    coord_c = Coord(.5,.5)
    coord_c2 = Coord(.25,.75)
    coord_c3 = Coord(2,1)
    coord_b = Coord(1,0)

    print(coord_c.__dict__)

    def myline(x):
        return Coord(x, x*-1 + 1)

    print((coord_a - coord_b))
    print((coord_c - coord_b))
    print(myline(-1).is_on_line(coord_a, coord_b))
    print(myline(-1).is_on_line(coord_b, coord_a))
    print(myline(0).is_on_line(coord_a, coord_b))
    print(myline(0).is_on_line(coord_b, coord_a))
    print(myline(.25).is_on_line(coord_a, coord_b))
    print(myline(.25).is_on_line(coord_b, coord_a))
    print(myline(.5).is_on_line(coord_a, coord_b))
    print(myline(.5).is_on_line(coord_b, coord_a))
    print(myline(1).is_on_line(coord_a, coord_b))
    print(myline(1).is_on_line(coord_b, coord_a))
    print(myline(2).is_on_line(coord_a, coord_b))
    print(myline(2).is_on_line(coord_b, coord_a))
    print("----")
    print(myline(.5).is_on_line(origin, Coord(1,1)))
    print(myline(.5).is_on_line(Coord(1,1), origin))
    print(myline(.55).is_on_line(origin, Coord(1,1)))
    print(myline(.55).is_on_line(Coord(1,1), origin))


if __name__ == "__main__":
    simpletest()
