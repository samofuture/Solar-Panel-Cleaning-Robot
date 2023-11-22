from roboclaw_python.roboclaw_3 import Roboclaw as rc
from gpiozero import Button
import numpy as np

# Useful resource for roboclaw library: https://resources.basicmicro.com/using-the-roboclaw-python-library/

# Found out that there is a big delay that happens when roboclaws can't be found at that address/serial port
class MotorControl:
    """
    The MotorControl class is designed to run as a wrapper for the roboclaw library and for more straight 
    forward readability in functions that need to move the motors
    """
    ppr: float = 1425.2                                     # Pulses per Revolution
    wheel_radius_cm = 2 * 2.54                              # The wheel radius in cm
    wheel_circumference_cm = 2 * wheel_radius_cm * np.pi    # The wheel circumference in cm
    brush_speed = 64
    auto_speed = 48
    def __init__(self, manual_button: Button) -> None:
        self.right_motors = rc("/dev/ttyACM2", 38400)   # This is the motor controller with the main housing
        self.left_motors = rc("/dev/ttyACM1", 38400)
        self.brush_motor = rc("/dev/ttyACM0", 38400)
        self.address = 0x80
        self.manual_button = manual_button

        right_status = self.right_motors.Open()
        left_status = self.left_motors.Open()
        brush_status = self.brush_motor.Open()

        print("Right Motors Status:", right_status)
        print("Left Motors Status:", left_status)
        print("Brush Motors Status:", brush_status)

    def _distance_to_count(self, distance_cm: float) -> float:
        """
        Returns the number of encoder ticks that is equivalent to the given distance in cm traveled
        """
        rotations = distance_cm / self.wheel_circumference_cm
        count = rotations * self.ppr
        return count
    
    def _count_to_distance(self, ticks) -> float:
        """
        Returns the distance in cm given the number of encoder ticks
        """
        rotations = ticks / self.ppr
        distance_cm = rotations * self.wheel_circumference_cm
        return distance_cm

    def move_robot_distance(self, distance_cm: float, brush_enabled: bool = False):
        """
        Moves the robot at a given speed (0 - 126) for some distance given in cm
        Distance is negative to go one way, and positive to go the other way
        Each time the function is called, the distance is relative to the robot
        """
        self.stop_robot()
        self.reset_encoders()
        remaining_distance = abs(distance_cm)
        if brush_enabled:
            self.set_brush_speed('R', self.brush_speed)
        curr_distance = 0
        while remaining_distance > 0 and not self.manual_button.is_pressed:
            if distance_cm < 0:
                self.move_robot('L', self.auto_speed)
            else:
                self.move_robot('R', self.auto_speed)

            curr_distance = self.find_distance()
            remaining_distance = abs(distance_cm) - curr_distance
        
        self.stop_robot()

        if self.manual_button.is_pressed:
            print(f"Stopped Robot at {curr_distance} with a remaining {remaining_distance} to travel")
            print("Manual Mode Engaged")
        else:
            print(f"Stopped Robot at {curr_distance}")

    def stop_robot(self):
        """ 
        Stops the Robot by setting their duty cycles to 0 (Should Coast (no active braking force))
        """
        self.right_motors.DutyM1M2(self.address, 0, 0)
        self.left_motors.DutyM1M2(self.address, 0, 0)
        self.brush_motor.DutyM1M2(self.address, 0, 0)

    def set_brush_speed(self, dir: str, speed: int) -> None:
        """
        Moves the brush only in a given direction ('R' or 'L') at a given speed (0 - 126)
        """
        # supposed to be 0-127 here but for some reason turning it backward runs into a
        # Input/output error with the roboclaw library when at the full 127
        if dir == 'R':
            self.brush_motor.ForwardM1(self.address, speed)
        elif dir == 'L':
            self.brush_motor.BackwardM1(self.address, speed)

    def set_right_speed(self, dir: str, speed: int):
        """
        Moves the right side of the robot in a direction at a speed
        """
        if dir == 'R':
            self.right_motors.ForwardM1(self.address, speed)
            self.right_motors.ForwardM2(self.address, speed)
        else:
            self.right_motors.BackwardM1(self.address, speed)
            self.right_motors.BackwardM2(self.address, speed)

    def set_left_speed(self, dir: str, speed: int):
        """
        Moves the left side of the robot in a direction at a speed
        """
        if dir == 'R':
            self.left_motors.ForwardM1(self.address, speed)
            self.left_motors.ForwardM2(self.address, speed)
        else:
            self.left_motors.BackwardM1(self.address, speed)
            self.left_motors.BackwardM2(self.address, speed)

    def move_robot(self, dir: str, speed: int):
        """
        Moves the robot at a given speed (0 - 126) in a given direction ('R' or 'L')
        """
        self.set_right_speed(dir, speed)
        self.set_left_speed(dir, speed)
    
    def read_encoders(self) -> tuple:
        """
        Reads the encoders of all of the motors and returns it in a tuple of lists
        """
        left_m1 = self.left_motors.ReadEncM1(self.address)
        left_m2 = self.left_motors.ReadEncM2(self.address)
        right_m1 = self.right_motors.ReadEncM1(self.address)
        right_m2 = self.right_motors.ReadEncM2(self.address)
        return ([left_m1, left_m2], [right_m1, right_m2])
    
    def reset_encoders(self) -> None:
        """
        Resets the encoder counts to 0
        """
        self.right_motors.ResetEncoders(self.address)
        self.left_motors.ResetEncoders(self.address)

    def find_distance(self, side: str = 'B') -> float:
        """
        Calculates the distance recorded on the encoders
        """
        left_enc, right_enc = self.read_encoders()
        left_dist = self._count_to_distance(np.mean(left_enc))
        right_dist = self._count_to_distance(np.mean(right_enc))
        if side == 'B':
            return np.mean([abs(left_dist), abs(right_dist)])
        elif side == 'L':
            return left_dist
        elif side == 'R':
            return right_dist
        else:
            return 0
        
    def clean_solar_panel(self):
        """
        The function to begin the autonomous cleaning routine
        """
        self.move_robot_distance(15, True)
