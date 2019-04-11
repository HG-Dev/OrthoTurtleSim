''' Main executable for the 2D turtle moving simultor. '''
import time
from turtlesim.world_render import WorldDrawer
from turtlesim.turtle import Turtle
from turtlesim.datatypes import Coord
from turtlesim.exceptions import ExitInterrupt

def main():
    """ Main body for starting up and updating simulation """
    # pylint: disable=no-member
    try:
        world = WorldDrawer()
        turtle = Turtle(world, Coord(0, 0))
        assert WorldDrawer.TURTLE in world.world_data[0]
        check_time = start_time = time.time()
        while True:
            #Tick check
            if time.time() - check_time > 1:
                check_time = check_time + 1
                if world.has_changed:
                    WorldDrawer.clear_screen()
                    print(int(check_time - start_time))
                    world.draw()
                turtle.update()
                if not turtle.moving:
                    raise ExitInterrupt

    except (KeyboardInterrupt, ExitInterrupt):
        print("Exiting")

if __name__ == "__main__":
    main()
