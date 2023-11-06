import time
import datetime as dt
from pytz import timezone
from skyfield import almanac
from skyfield.api import N, W, wgs84, load
from calendar import timegm

LATITUDE = 35.302078
LONGITUDE = 80.731392 # W is negative

def get_current_time() -> float:
    return time.clock_gettime(0)

def epoch_to_date(epoch: float) -> str:

    date_str = time.strftime('%Y-%m-%d', time.localtime(epoch))

    return date_str

def date_to_epoch(date: str) -> int:
    datetime_obj = time.strptime(date, "%Y-%m-%d %H:%M:%S")

    epoch = timegm(datetime_obj)
    
    return epoch

def get_solar_noon() -> str:
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