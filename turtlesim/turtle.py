''' Autonomous nearly-blind thing for demonstrating 2D navigation '''
# Note to self: there's no easy way to clear the screen on windows/IDLE it seems.
# TODO: Find out why heading changes from IntEnum to regular int
from dataclasses import dataclass
from turtlesim.datatypes import Coord, HeadingType, Heading
from turtlesim.world_render import WorldDrawer
from time import time



class Turtle:
    ''' Simple moving thing that is aware of squares above, below, and in front of it. '''

    def __init__(self, world: WorldDrawer, spawn_coord: Coord()):
        self.location = spawn_coord
        self.heading = Heading() #or "facing": does not include up or down as turtles can not face upwards
        self.destination = spawn_coord + Coord(5, 5)
        self.world = world
        self.speed = 1 #squares per second
        self.moving = False
        self.bumped = False
        self.learned_paths = []
        self.proposed_paths = []
        world.set_cell(spawn_coord, WorldDrawer.TURTLE)

    def try_move(self, heading: Heading):
        """
        Move the turtle in four possible directions:
        forward, backward, up, or down. Return boolean success.
        """
        self.world.get_cell(self.location + heading.vector)


    def update(self):
        """
        Tick function called so that turtle makes incremental
        movement and decisions.
        """
        dist_vector = self.destination - self.location
        print(dist_vector)
        print(HeadingType(self.heading.index))
        moved = False
        self.moving = self.location != self.destination
        #Aim for the route that requires the least number of turns
        if self.moving:
            move_ideas = dist_vector.sorted_ortho_normals
            for normal in move_ideas:
                if self.world.get_cell(self.location + normal) != WorldDrawer.EMPTY:
                    continue
                elif Heading.from_vector(normal) != self.heading:
                    # Must turn first
                    self.turn_towards(Heading.from_vector(normal))
                    self.world.set_cell(self.location, WorldDrawer.TURTLE + self.heading.index, safe=False)
                    break
                elif self.world.set_cell(self.location + normal, WorldDrawer.TURTLE + self.heading.index):
                    self.world.set_cell(self.location, WorldDrawer.EMPTY, safe=False)
                    self.location = self.location + normal
                    moved = True
                    break

    def sense(self):
        """
        Returns a tuple of three booleans representing whether or not
        something exists in the surrounding squares: front, up, down
        """
        front = self.world.get_cell(self.location + self.heading.vector)
        return front

    def turn_towards(self, desired_heading: Heading):
        """
        Advances heading one cardinal step towards a desired target heading.
        Returns true if complete; false if more turning is required.
        """
        if self.heading == desired_heading:
            return False
        random = time() % 2
        x_axis = (HeadingType.EAST, HeadingType.WEST)
        y_axis = (HeadingType.NORTH, HeadingType.SOUTH)
        new_heading = desired_heading
        one_turn = True
        if self.heading in x_axis and desired_heading in x_axis:
            new_heading = y_axis[random]
            one_turn = False
        elif self.heading in y_axis and desired_heading in y_axis:
            new_heading = x_axis[random]
            one_turn = False
        self.heading = new_heading
        return one_turn

#Proposed functionality: is cell on learned or proposed path
'''
class Event(list):
    """Event subscription.


            #Temporary implementation: try to move towards destination
        dist_vector = self.destination - self.location
        self.moving = self.location != self.destination
        if self.moving:
            move_ideas = []
            if abs(dist_vector.x) > abs(dist_vector.y):
                move_ideas.append(dist_vector.ortho_normal.just_x)
                move_ideas.append(dist_vector.ortho_normal.just_y)
            else:
                move_ideas.append(dist_vector.ortho_normal.just_y)
                move_ideas.append(dist_vector.ortho_normal.just_x)
            if self.world.set_cell(self.location+move_ideas[0], WorldDrawer.TURTLE + self.heading.index):
                self.world.set_cell(self.location, WorldDrawer.EMPTY, False)
                self.location = self.location + move_ideas[0]
            elif self.world.set_cell(self.location+move_ideas[1], WorldDrawer.TURTLE + self.heading.index):
                self.world.set_cell(self.location, WorldDrawer.EMPTY, False)
                self.location = self.location + move_ideas[1]
            else:
                print("Couldn't move")

    A list of callable objects. Calling an instance of this will cause a
    call to each item in the list in ascending order by index.

    Example Usage:
    >>> def f(x):
    ...     print 'f(%s)' % x
    >>> def g(x):
    ...     print 'g(%s)' % x
    >>> e = Event()
    >>> e()
    >>> e.append(f)
    >>> e(123)
    f(123)
    >>> e.remove(f)
    >>> e()
    >>> e += (f, g)
    >>> e(10)
    f(10)
    g(10)
    >>> del e[0]
    >>> e(2)
    g(2)

    """
    def __call__(self, *args, **kwargs):
        for f in self:
            f(*args, **kwargs)

    def __repr__(self):
        return "Event(%s)" % list.__repr__(self)
'''
