from roboclaw_python.roboclaw_3 import Roboclaw as rc
import numpy as np

# Useful resource for roboclaw library: https://resources.basicmicro.com/using-the-roboclaw-python-library/

# Found out that there is a big delay that happens when roboclaws can't be found at that address
class MotorControl:
    ppr: float = 1425.2 # Pulses per Revolution
    def __init__(self) -> None:
        self.right_motors = rc("/dev/ttyACM0", 38400)
        self.left_motors = rc("/dev/ttyACM1", 38400)
        self.brush_motor = rc("/dev/ttyACM2", 38400)
        self.left_motors = 0x81
        self.right_motors = 0x82
        self.brush_motor = 0x82 # Probably 0x81
        result = self.motors.Open()
        print(result)
        # Reverse Direction of motors if necessary here

    def _distance_to_count(self, distance_cm: float, radius_cm: float) -> float:
        circumference = 2 * radius_cm * np.pi
        rotations = distance_cm / circumference
        count = rotations * self.ppr
        return count
    
    def _count_to_distance(self, ticks, radius_cm: float) -> float:
        circumference = 2 * radius_cm * np.pi
        rotations = ticks / self.ppr
        distance_cm = rotations * circumference
        return distance_cm

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

    def read_encoders(self):
        return self.motors.ReadEncM2(self.brush_motor), 0
    
    def _read_encoders(self) -> tuple:
        left_m1 = self.motors.ReadEncM1(self.left_motors)
        left_m2 = self.motors.ReadEncM2(self.left_motors)
        right_m1 = self.motors.ReadEncM1(self.right_motors)
        right_m2 = self.motors.ReadEncM2(self.right_motors)
        return ([left_m1, left_m2], [right_m1, right_m2])

    def find_distance(self, side: str = 'B') -> float:
        left_enc, right_enc = self.read_encoders()
        wheel_radius = 4*2.54/2
        left_dist = self._count_to_distance(np.mean(left_enc), wheel_radius)
        right_dist = self._count_to_distance(np.mean(right_enc), wheel_radius)
        if side == 'B':
            return np.mean([left_dist, right_dist])
        elif side == 'L':
            return left_dist
        elif side == 'R':
            return right_dist
        else:
            return 0
        
    def clean_solar_panel(self):
        