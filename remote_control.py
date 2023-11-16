import numpy as np
from gpiozero import Button
from pyPS4Controller.controller import Controller
from motor_control import MotorControl

class MyController(Controller):

    def __init__(self, manual_button: Button, **kwargs):
        Controller.__init__(self, **kwargs)
        self.mc = motor_controller
        self.brush_dir: str = 'R'
        self.button: Button = manual_button

    def on_x_press(self):
        print("Stop")
        self.mc.stop_robot()

    def on_triangle_press(self):
        if self.brush_dir == 'L':
            self.brush_dir = 'R'
        else:
            self.brush_dir = 'L'

    def on_circle_release(self):
       self.mc.move_brush('R', 67)

    def on_R2_press(self, value):
        # supposed to be 0-127 here but for some reason turning it 'L' runs into a
        # Input/output error with the roboclaw library 
        print(value)
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

    def on_R1_press(self):
        distance_traveled = self.mc.find_distance('L')
        print(distance_traveled)
        return distance_traveled

    def on_down_arrow_press(self):
        print("here")
        return None
    
    def on_playstation_button_press(self):
        if not self.button.is_pressed:
            self.stop = True