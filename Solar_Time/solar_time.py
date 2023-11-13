import time
import datetime as dt
from pytz import timezone
from astral.sun import sun
from astral import LocationInfo

LATITUDE = 35.302078    # N is positive
LONGITUDE = -80.731392  # W is negative

def get_current_time() -> float:
    return time.clock_gettime(0)

def epoch_to_date(epoch: float) -> str:
    date_str = time.strftime('%Y-%m-%d', time.localtime(epoch))
    return date_str

def datetime_to_epoch(date: dt) -> int:
    return int(date.timestamp())

def get_solar_noon(time_zone: str = 'US/Eastern') -> str:
    location = LocationInfo("Charlotte", "USA", "UTC", LATITUDE, LONGITUDE)
    today_date = dt.datetime.now().date()
    solar_noon_utc = sun(location.observer, date=today_date)['noon']
    solar_noon = solar_noon_utc.astimezone(timezone(time_zone))

    return solar_noon

if __name__ == '__main__':
    start = time.clock_gettime(0)

    solar_noon = get_solar_noon()

    print(start)
    print(solar_noon)