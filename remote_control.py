import numpy as np
from gpiozero import Button
from pyPS4Controller.controller import Controller
from motor_control import MotorControl

class MyController(Controller):
    """
    The MyController class is overloading the functions provided by the pyPS4Controller library
    and mapping the controls to various actions on the robot
    """

    def __init__(self, motor_controller: MotorControl, manual_button: Button, **kwargs):
        Controller.__init__(self, **kwargs)
        self.mc = motor_controller
        self.button: Button = manual_button

    def on_x_press(self):
        """
        When the x button is pressed, stop the robot
        """
        print("Stop")
        self.mc.stop_robot()

    def on_R2_press(self, value):
        """
        When the right trigger is pressed down, move the brush motor right
        Value is how much the trigger is being pressed
        """
        # supposed to be 0-127 here but for some reason turning it 'L' runs into a
        # Input/output error with the roboclaw library when at the full 127
        print(value)
        speed = int(np.interp(value, [-32767, 32767], [0, 126]))
        self.mc.move_brush('R', speed)

    def on_R2_release(self):
        """
        When the right trigger is released stop the brush motor
        """
        self.mc.move_brush('R', 0)

    def on_L2_press(self, value):
        """
        When the left trigger is pressed down, move the brush motor left
        Value is how much the trigger is being pressed
        """
        print(value)
        speed = int(np.interp(value, [-32767, 32767], [0, 126]))
        self.mc.move_brush('L', speed)

    def on_L2_release(self):
        """
        When the left trigger is released stop the brush motor
        """
        self.mc.move_brush('L', 0)
    
    def on_R3_up(self, value):
        """
        When the right joystick is being moved up, move the robot accordingly
        Value is how much the joystick is being moved
        """
        value = abs(value)
        speed = int(np.interp(value, [0, 32767], [0, 126]))
        self.mc.move_robot('R', speed)

    def on_R3_down(self, value):
        """
        When the right joystick is being moved down, move the robot accordingly
        Value is how much the joystick is being moved
        """
        speed = int(np.interp(value, [0, 32767], [0, 126]))
        self.mc.move_robot('L', speed)

    def on_R3_y_at_rest(self):
        """
        When the right joystick isn't being moved stop the robot
        """
        self.mc.stop_robot()

    def on_R1_press(self):
        """
        When the right bumper is pressed print the distance the robot
        has traveled to the console
        """
        distance_traveled = self.mc.find_distance()
        print(distance_traveled)
        return distance_traveled
    
    def on_playstation_button_press(self):
        """
        Stop listening to the controller if the manual button isn't being pressed
        """
        if not self.button.is_pressed:
            self.mc.stop_robot()
            self.stop = True
