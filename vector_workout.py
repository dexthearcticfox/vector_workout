import anki_vector
from anki_vector.events import Events
from anki_vector.util import degrees, distance_mm, speed_mmps
import functools
import threading
import time
animation = 'anim_fistbump_success_01'

def main():
    evt = threading.Event()

    def on_tapped_cube(robot, event_type, event):
        robot.conn.request_control()
        robot.events.unsubscribe(on_tapped_cube, Events.object_tapped)
        print(robot.lift_height_mm)
        if robot.lift_height_mm > 50:
            time.sleep(1)
            robot.events.subscribe(on_tapped_cube, Events.object_tapped)
        else:
            response = robot.behavior.dock_with_cube(
                robot.world.connected_light_cube,
                num_retries=3)
            time.sleep(1.0)
            robot.motors.set_lift_motor(2)
            robot.say_text("1")
            robot.motors.set_lift_motor(-2)
            time.sleep(2)
            robot.motors.set_lift_motor(2)
            robot.say_text("2")
            robot.motors.set_lift_motor(-2)
            time.sleep(2)
            robot.motors.set_lift_motor(2)
            robot.say_text("3")
            robot.motors.set_lift_motor(-2)
            robot.anim.play_animation(animation)
            robot.events.subscribe(on_tapped_cube, Events.object_tapped)
        evt.set()

    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial) as robot:
        robot.conn.request_control()
        print("Connecting...")
        robot.behavior.set_head_angle(degrees(0.0))
        robot.world.connect_cube()
        print("Connected")
        on_tapped_cube = functools.partial(on_tapped_cube, robot)
        robot.events.subscribe(on_tapped_cube, Events.object_tapped)
        print("Tap Vector's cube")
        j = 0
        while j < 30:
            time.sleep(1.0)
            j += 1

if __name__ == '__main__':
    main()
