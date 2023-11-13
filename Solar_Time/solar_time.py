import time
import datetime as dt
from pytz import timezone
from skyfield import almanac
from skyfield.api import N, W, wgs84, load
from astral.sun import sun
from astral import LocationInfo

LATITUDE = 35.302078
LONGITUDE = 80.731392 # W is negative

def get_current_time() -> float:
    return time.clock_gettime(0)

def epoch_to_date(epoch: float) -> str:

    date_str = time.strftime('%Y-%m-%d', time.localtime(epoch))

    return date_str

def date_to_epoch(date: str, time_zone: str = 'US/Eastern') -> int:
    datetime_obj = dt.datetime.strptime(date, "%Y-%m-%d %H:%M:%S %Z")

    datetime_obj = timezone(time_zone).localize(datetime_obj)
    
    epoch = int(datetime_obj.timestamp())
    return epoch

def get_solar_noon(time_zone: str = 'US/Eastern') -> str:
    location = LocationInfo("Charlotte", "USA", "UTC", LATITUDE, -LONGITUDE)
    today_date = dt.datetime.now().date()
    solar_noon_utc = sun(location.observer, date=today_date)['noon']
    print(solar_noon_utc)
    solar_noon_str = solar_noon_utc.strftime('%Y-%m-%d %H:%M:%S %Z')
    # solar_noon_local = timezone(time_zone).localize(solar_noon_utc)
    print(date_to_epoch(solar_noon_str))
    return solar_noon

def _get_solar_noon() -> str:
    # This Method comes from here: 
    # https://rhodesmill.org/skyfield/examples.html

    zone = timezone('US/Eastern')
    now = zone.localize(dt.datetime.now())
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    next_midnight = midnight + dt.timedelta(days=1)

    ts = load.timescale()
    t0 = ts.from_datetime(midnight)
    t1 = ts.from_datetime(next_midnight)
    eph = load('Solar_Time/de421.bsp')
    bluffton = wgs84.latlon(LATITUDE * N, LONGITUDE * W)

    f = almanac.meridian_transits(eph, eph['Sun'], bluffton)
    times, events = almanac.find_discrete(t0, t1, f)

    # Select transits instead of antitransits.
    times = times[events == 1]

    t = times[0]
    tstr = str(t.astimezone(zone))[:19]
    epoch = date_to_epoch(tstr)

    return tstr


if __name__ == '__main__':
    start = time.clock_gettime(0)

    solar_noon = get_solar_noon()

    print(start)
    print(solar_noon)