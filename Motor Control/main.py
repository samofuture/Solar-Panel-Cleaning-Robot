from roboclaw_python.roboclaw_3 import Roboclaw as rc
from pyPS4Controller.controller import Controller
import numpy as np

# Useful resource for roboclaw library: https://resources.basicmicro.com/using-the-roboclaw-python-library/

# Found out that there is a big delay that happens when roboclaws can't be found at that address
class MotorControl:
    ppr: float = 1425.2
    def __init__(self) -> None:
        self.motors = rc("/dev/ttyACM0", 38400)
        self.left_motors = 0x81
        self.right_motors = 0x81
        self.brush_motor = 0x80
        self.motors.Open()
        # Reverse Direction of motors if necessary here

    def _distance_to_count(self, distance_cm: float, radius_cm: float) -> float:
        circumference = 2 * radius_cm * np.pi
        rotations = distance_cm / circumference
        count = rotations * self.ppr
        return count

    def move_robot_distance(self, dir: str, speed: int, distance_cm: float):
        # Moves the robot 
        pos = self._distance_to_count(distance_cm, 4*2.54)
        accel = 1
        deccel = 1
        buffer = 1

        # Need to test if these execute simultaneously or not
        self.motors.SpeedAccelDeccelPositionM1M2(self.left_motors,accel,speed,deccel,pos,
                                                 accel,speed,deccel,pos,buffer)
        self.motors.SpeedAccelDeccelPositionM1M2(self.right_motors,accel,speed,deccel,pos,
                                                 accel,speed,deccel,pos,buffer)

    def stop_robot(self):
        # Stops the Robot (Should Coast)
        # Commented out for now to test a single one
        # self.motors.DutyM1M2(self.left_motors, 0, 0)
        # self.motors.DutyM1M2(self.right_motors, 0, 0)
        self.motors.DutyM1M2(self.brush_motor, 0, 0)

    def move_brush(self, dir: str, speed: int) -> None:
        # Moves the Brush
        if dir == 'L':
            self.motors.ForwardM1(self.brush_motor, speed)
        elif dir == 'R':
            self.motors.BackwardM1(self.brush_motor, speed)

    def move_robot(self, dir: str, speed: int):
        # Moves robot manually
        if dir == 'R':
            self.motors.ForwardMixed(self.brush_motor, speed)
        elif dir == 'L':
            self.motors.BackwardMixed(self.brush_motor, speed)
        # self.motors.ForwardBackwardMixed(self.brush_motor, speed)

class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        self.mc = MotorControl()
        self.brush_dir: str = 'R'

    def on_x_press(self):
        print("Stop")
        self.mc.stop_robot()

    def on_triangle_press(self):
        if self.brush_dir == 'L':
            self.brush_dir = 'R'
        else:
            self.brush_dir = 'L'

    def on_circle_release(self):
       print("Goodbye world")
       self.mc.move_brush('R', 67)

    def on_R2_press(self, value):
        # supposed to be 0-127 here but for some reason turning it 'L' runs into a
        # Input/output error with the roboclaw library 
        speed = int(np.interp(value, [-32767, 32767], [0, 126]))
        # print(speed)
        self.mc.move_brush(self.brush_dir, speed)

    def on_R2_release(self):
        self.mc.move_brush(self.brush_dir, 0)

    def on_R3_up(self, value):
        value = abs(value)
        speed = int(np.interp(value, [0, 32767], [0, 126]))
        self.mc.move_robot('R', speed)

    def on_R3_down(self, value):
        speed = int(np.interp(value, [0, 32767], [0, 126]))
        self.mc.move_robot('L', speed)

    def on_R3_y_at_rest(self):
        self.mc.move_robot('R', 0)

controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
# you can start listening before controller is paired, as long as you pair it within the timeout window
controller.listen(timeout=60)