# Check for which mode we need

# --> If Autonomous, check camera
    # If Dirty, Trigger Cleaning Routine
    # Reset Timer to take Picture

# --> If Manual, Receive input from the controller

import time
import datetime
from astral.sun import sun
from astral import LocationInfo


LATITUDE = 35.302078
LONGITUDE = -80.731392

def epoch_to_date(epoch: float) -> str:

    date_str = time.strftime('%Y-%m-%d', time.localtime(epoch))

    return date_str

def get_solar_noon() -> float:
    location = LocationInfo("Charlotte", "USA", LATITUDE, LONGITUDE)

    current_date = datetime.date.today()

    s = sun(location.observer, date=current_date)
    solar_noon = s['noon']

    # print("Solar Noon (Apparent Zenith) Time:", solar_noon)
    
    return solar_noon.timestamp()


if __name__ == '__main__':
    start = time.clock_gettime(0)
    date = epoch_to_date(start)

    solar_noon = get_solar_noon(date)
    print(solar_noon)