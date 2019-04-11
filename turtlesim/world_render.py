''' Grid drawing functions. '''
# Note to self: there's no easy way to clear the screen on windows/IDLE it seems.
from time import sleep
from math import sqrt
from copy import deepcopy
import terminaltables
from turtlesim.datatypes import Coord
TERMINAL_HEIGHT = 40
class WorldDrawer(terminaltables.SingleTable):
    """
    A class that wraps the terminaltables library for converting simpler
    2D block world representations into a visually comprehensible format.
    """
    EMPTY = 0
    TURTLE = 255
    SOLID = 1
    PATH_START = 200
    PATH_HORIZ = 201
    PATH_VERT = 202
    CELL_STRS = {
        0: "   \n   ",
        1: "███\n███",
        200: " ^ \n U ",
        201: "___\n   ",
        202: " | \n | ",
        255: "┌╥┐\n└╨┘",
        256: "┌─╖\n└─╜",
        257: "╓─┐\n╙─┘",
        258: "┌─┐\n╘═╛",
        259: "╒═╕\n└─┘"
    }

    def __init__(self, size_x=12, size_y=10):
        self._size_x = size_x
        self._size_y = size_y
        super(WorldDrawer, self).__init__(None)
        self.debug_data = WorldDrawer.generate_world(self, empty=True)
        self.world_data = WorldDrawer.generate_world(self)
        self.table_data = WorldDrawer.convert_world_data(self.world_data)
        self.prev_world_data = [[]]
        self.inner_heading_row_border = False
        self.inner_row_border = False
        self.inner_column_border = False
        self.show_debug = True

    def generate_world(self, empty=False, surface_y=2, arc_center=None, tunnel_width=2.5):
        ''' Creates a 2D world for navigation testing '''
        output_world_data = [[WorldDrawer.EMPTY for _ in range(self._size_x)] for _ in range(self._size_y)]
        if not empty:
            tunnel_arc_center = arc_center or Coord(self._size_x/2, surface_y)
            for y, row in enumerate(output_world_data):
                for x in range(self._size_x):
                    row[x] = 1
                    if (
                            y < surface_y or
                            tunnel_width < tunnel_arc_center.dist_to(Coord(x,y)) < tunnel_width * 2
                    ):
                        row[x] = 0

        return output_world_data

    @property
    def has_changed(self):
        """
        Returns True if last_printed_table_data is no longer
        representative of the world's current state.
        """
        return self.prev_world_data != self.world_data

    @staticmethod
    def convert_world_data(world_data):
        ''' Converts a given 2D table of world data into a printable set of table data '''
        return [list(map(lambda x: WorldDrawer.CELL_STRS[x], row)) for row in world_data]

    @staticmethod
    def add_debug_data(table_data, debug_overlay):
        ''' Converts a given 2D table of world data into a printable set of table data '''
        output = table_data
        assert len(table_data) == len(debug_overlay)
        for y, row in enumerate(output):
            for x, cell in enumerate(row):
                if cell == WorldDrawer.EMPTY:
                    output[y][x] = debug_overlay[y][x]

        return output

    @staticmethod
    def clear_screen():
        ''' A cheap method of scrolling down until nothing can be seen. '''
        print("".join(["\n" for _ in range(TERMINAL_HEIGHT)]))

    def set_cell(self, coord: Coord, content_code: int, safe=True):
        """ Sets the contents of a cell in world_data. In safe, mode only Empty cells can be changed. """
        if not (0 <= coord.x < self._size_x) or not (0 <= coord.y < self._size_y):
            return False
        if safe and self.world_data[coord.y][coord.x] != WorldDrawer.EMPTY:
            return False
        self.world_data[coord.y][coord.x] = content_code
        return True

    def get_cell(self, coord: Coord):
        """ Returns the world_data contents at a given coordinate. """
        if not (0 <= coord.x < self._size_x) or not (0 <= coord.y < self._size_y):
            return None
        return self.world_data[coord.y][coord.x]

    def draw(self):
        ''' Refreshes the base class's table_data using self.world_data and prints it '''
        self.prev_world_data = deepcopy(self.world_data)
        self.table_data = WorldDrawer.convert_world_data(self.world_data)
        if self.show_debug:
            self.table_data = WorldDrawer.add_debug_data(self.table_data, self.debug_data)
        print(self.table)

def simpletest():
    ''' Simple test of GridDrawer used for feature development '''
    world = WorldDrawer()
    world.draw()
    world.world_data[0][0] = 255
    sleep(1)
    world.draw()

if __name__ == "__main__":
    simpletest()
