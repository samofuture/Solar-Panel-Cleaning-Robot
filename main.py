"""
This is the script responsible for running the robot. There are some pieces of code that will
need to be updated in the final implementation of the robot, and those are marked with <-----

HOW TO RUN THE ROBOT
1. Turn the E-Stop button to enable power to go to the Raspberry Pi and the Roboclaws
2. Connect to the Raspberry Pi and run this script
3. If you want to be in manual mode, press the black button and connect the controller
    Controls are pretty self explanatory, but here they are anyways:
    a. The right joystick controls the robot movement
    b. The triggers control the brush movement
    c. Rest of the controls are in the remote_control.py file
"""
import os
import sys
vision_dir = os.path.abspath('Vision')
sys.path.append(vision_dir)
time_dir = os.path.abspath('Solar_Time')
sys.path.append(time_dir)
from gpiozero import Button
from time import sleep

import remote_control as rc
#from Solar_Time import solar_time as st    # <----- Enable this line
from Vision import color_analyzer as ca
from motor_control import MotorControl as mc

if __name__ == '__main__':
    # This sets it up so that the button is 'pressed' if it is connected to ground
    manual_button = Button(4)
    # print(f"Next Solar Noon: {st.get_solar_noon()}")
    # next_solar_noon = st.date_to_epoch(st.get_solar_noon())   # <----- Enable this line
    need_to_clean: bool = False
    next_solar_noon = 0
    curr_time = 1000000000000   # <----- Should probably set this to 0
    print(f"Next Solar Noon: {next_solar_noon}")
    while True:
        # curr_time = st.get_current_time() # <------- Enable this line
        curr_time += 1  # <--------- Get rid of this line

        # If Manual Button is pressed
        if manual_button.is_pressed:
            motor_controller = mc(manual_button)

            controller = rc.MyController(motor_controller=motor_controller, manual_button=manual_button, interface="/dev/input/js0", connecting_using_ds4drv=False)
            # you can start listening before controller is paired, as long as you pair it within the timeout window
            controller.listen(timeout=30, on_connect=print("Connected to Controller"), on_disconnect=print("Disconnected from Controller"))
            
        # If it's time to check the panel
        elif (curr_time - next_solar_noon > 0 and curr_time - next_solar_noon < 60):
            # TODO: Figure out how to take a picture here
            new_img = None
            if not need_to_clean and ca.panel_is_dirty(new_img):
                need_to_clean = True
            
        # If it's time to clean the panel
        elif need_to_clean:
            mc(manual_button).clean_solar_panel()
            # next_solar_noon = st.datetime_to_epoch(st.get_solar_noon())   # <----- Enable this line
            print(f"Next Solar Noon: {next_solar_noon}")
            need_to_clean = False
            
        print(f"Current Time: {curr_time}")
        sleep(0.5)
