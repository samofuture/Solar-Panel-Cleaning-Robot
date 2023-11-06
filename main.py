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
import remote_control as rc
from Solar_Time import solar_time as st
from Vision import color_analyzer as ca
from motor_control import MotorControl as mc

if __name__ == '__main__':
    next_solar_noon = st.date_to_epoch(st.get_solar_noon())
    need_to_clean: bool = False
    while True:
        curr_time = st.get_current_time()
        
        # If Manual Button is pressed
        # TODO: Read button input
        if True:
            controller = rc.MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
            # you can start listening before controller is paired, as long as you pair it within the timeout window
            controller.listen(timeout=60)
            # can add connect/disconnect functions to listen
            # holding ps button on controller for 10 seconds should turn off the controller
        # If it's time to check the panel
        elif (curr_time - next_solar_noon > 0 and curr_time - next_solar_noon < 60):
            # TODO: Figure out how to take a picture here
            new_img = None
            if not need_to_clean and ca.panel_is_dirty(new_img):
                need_to_clean = True
            
        # If it's time to clean the panel
        elif need_to_clean:
            mc.clean_solar_panel()