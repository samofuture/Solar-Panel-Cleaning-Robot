# Check for which mode we need

# --> If Autonomous, check camera
    # If Dirty, Trigger Cleaning Routine
    # Reset Timer to take Picture

# --> If Manual, Receive input from the controller
import os
import sys
vision_dir = os.path.abspath('Vision')
sys.path.append(vision_dir)
time_dir = os.path.abspath('Solar_Time')
sys.path.append(time_dir)
from gpiozero import Button
from time import sleep

import remote_control as rc
#from Solar_Time import solar_time as st
from Vision import color_analyzer as ca
from motor_control import MotorControl as mc

if __name__ == '__main__':
    # This sets it up so that the button is 'pressed' if it is connected to ground
    manual_button = Button(4)
    #print(f"Next Solar Noon: {st.get_solar_noon()}")
    #next_solar_noon = st.date_to_epoch(st.get_solar_noon())
    need_to_clean: bool = True
    next_solar_noon = 0
    curr_time = 1000000000000
    print(f"Next Solar Noon: {next_solar_noon}")
    while True:
        #curr_time = st.get_current_time()
        curr_time += 1
        # If Manual Button is pressed
        if manual_button.is_pressed:
            motor_controller = mc(manual_button)
            motor_controller.clean_solar_panel()

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
            # next_solar_noon = st.datetime_to_epoch(st.get_solar_noon())
            print(f"Next Solar Noon: {next_solar_noon}")
            need_to_clean = False
            
        print(f"Current Time: {curr_time}")
        sleep(0.5)
