#!/usr/bin/python
# Filename: utilModule.py
from datetime import datetime
import pytz
import dateparser
from lib import constants

def ms2date(ms):
    return datetime.fromtimestamp(ms/1000.0)

def date_to_milliseconds(date_str):
    """Convert UTC date to milliseconds
    If using offset strings add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"
    See dateparse docs for formats http://dateparser.readthedocs.io/en/latest/
    :param date_str: date in readable format, i.e. "January 01, 2018", "11 hours ago UTC", "now UTC"
    :type date_str: str
    """
    # get epoch value in UTC
    epoch = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
    # parse our date string
    d = dateparser.parse(date_str)
    # if the date is not timezone aware apply UTC timezone
    if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
        d = d.replace(tzinfo=pytz.utc)

    # return the difference in time
    return int((d - epoch).total_seconds() * 1000.0)

def interval_to_milliseconds(interval):
    """Convert a Binance interval string to milliseconds
    :param interval: Binance interval string 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w
    :type interval: str
    :return:
         None if unit not one of m, h, d or w
         None if string not in correct format
         int value of interval in milliseconds
    """
    ms = None
    seconds_per_unit = {
        "m": 60,
        "h": 60 * 60,
        "d": 24 * 60 * 60,
        "w": 7 * 24 * 60 * 60
    }

    unit = interval[-1]
    if unit in seconds_per_unit:
        try:
            ms = int(interval[:-1]) * seconds_per_unit[unit] * 1000
        except ValueError:
            print('errorrrrrrrrr when converting to ms')
            pass
    return ms

def writeList2File(klinelist, interval):
    # open a file with filename including symbol, interval and start and end converted to milliseconds
    with open(
        "Binance_{}_{}_{}-{}.txt".format(
            constants.SYMBOL, 
            interval, 
            date_to_milliseconds(constants.START),
            date_to_milliseconds(constants.END)
        ),
        'w' # set file write mode
    ) as f:
        # f.write(json.dumps(klines))
        f.write('\n'.join(str(k) for k in klinelist)) # using generator expression to turn list of objects into string.

# end of utilModule