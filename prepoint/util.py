from datetime import datetime, timezone, timedelta
import math

import ephem

__author__ = "Eric Dose :: New Mexico Mira Project, Albuquerque"


def calc_az_alt(longitude, latitude, ra, dec, datetime_utc):
    """  Returns azimuth and altitude for sky position (RA and Dec)
         at a given earth longitude and Latitude, at a given date and time (in UTC).
    :param longitude: longitude of earth position, in degrees east=positive [float].
    :param latitude: latitude of earth position, in degrees north=positive [float].
    :param ra: right ascension of sky position, in degrees [float].
    :param dec: declination of sky position, in degrees [float].
    :param datetime_utc: date and time for which to calculate az and alt, in UTC [datetime object].
    :return: 2-tuple of azimuth, altitude in degrees [2-tuple of floats].
    adapted from photrix August 2018.
    """
#     return 1.0, 2.0  # dummy line for testing only.

    obs = ephem.Observer()  # for local use.
    obs.lon = degrees_as_hex(longitude)
    obs.lat = degrees_as_hex(latitude)
    obs.date = datetime_utc

    target_ephem = ephem.FixedBody()  # so named to suggest restricting its use to ephem.
    target_ephem._epoch = '2000'
    target_ephem._ra = ra_as_hours(ra)
    target_ephem._dec = degrees_as_hex(dec)
    target_ephem.compute(obs)
    return target_ephem.az * 180 / math.pi, target_ephem.alt * 180 / math.pi


def next_datetime_from_time_string(time_text):
    time_list = parse_hex(time_text)
    if len(time_list) != 3:
        return None
    try:
        hour = int(time_list[0])
        minute = int(time_list[1])
        second = int(time_list[2])
    except ValueError:
        return None
    if not (0 <= hour <= 23):
        return None
    if not (0 <= minute <= 59):
        return None
    if not (0 <= second <= 59):
        return None
    now = datetime.now(timezone.utc)
    raw_time = datetime(year=now.year, month=now.month, day=now.day,
                        hour=hour, minute=minute, second=second).replace(tzinfo=timezone.utc)
    if raw_time > now:
        return raw_time
    else:
        return raw_time + timedelta(days=1)


PARSE_TEXT__________________________ = 0


def parse_hex(hex_string):
    """
    Helper function for RA and Dec parsing, takes hex string, returns list of floats.
    :param hex_string: string in either full hex ("12:34:56.7777" or "12 34 56.7777"),
               or degrees ("234.55")
    :return: list of strings representing floats (hours:min:sec or deg:arcmin:arcsec).
    from photrix August 2018.
    """
    colon_list = hex_string.split(':')
    space_list = hex_string.split()  # multiple spaces act as one delimiter
    if len(colon_list) >= len(space_list):
        return [x.strip() for x in colon_list]
    return space_list


def hex_degrees_as_degrees(hex_degrees_string):
    """
    :param hex_degrees_string: string in either full hex ("-12:34:56.7777", or "-12 34 56.7777"),
        or degrees ("-24.55")
    :return float of degrees (not limited)
    adapted from photrix.util August 2018; added return=None for unparseable string,
        or for minutes or seconds = negative or >=60.
    """
    hex_list = parse_hex(hex_degrees_string)
    if hex_list[0].startswith("-"):
        sign = -1
    else:
        sign = 1
    try:
        if len(hex_list) == 1:
            dec_degrees = float(hex_list[0])  # input assumed to be in degrees.
        elif len(hex_list) == 2:
            if (int(hex_list[1]) >= 60) or (int(hex_list[1]) < 0):
                return None
            dec_degrees = sign * (abs(int(hex_list[0])) + int(hex_list[1])/60.0)  # input is hex.
        else:
            if (int(hex_list[1]) >= 60) or (int(hex_list[1]) < 0) or\
               (float(hex_list[2]) >= 60) or (float(hex_list[2]) < 0):
                return None
            dec_degrees = sign * (abs(int(hex_list[0])) + int(hex_list[1]) / 60.0 +
                                  float(hex_list[2])/3600.0)  # input is hex.
    except ValueError:
        return None
    return dec_degrees


def longitude_as_degrees(longitude_string):
    degrees = hex_degrees_as_degrees(longitude_string)
    if degrees is None:
        return None
    if not (-180 <= degrees <= +180):
        return None
    return degrees


def latitude_as_degrees(latitude_string):
    degrees = hex_degrees_as_degrees(latitude_string)
    if degrees is None:
        return None
    if not (-90 <= degrees <= +90):
        return None
    return degrees


def ra_as_degrees(ra_string):
    """
    :param ra_string: string in either  hex ("12:34:56.7777" or "12 34 56.7777" or "12 34"),
               but not in degrees in this implementation.
    :return float of Right Ascension in degrees between 0 and 360.
    adapted from photrix.util August 2018; added return=None for unparseable string,
        or for minutes or seconds = negative or >=60.
    adapted heavily from photrix, August 2018.
    """
    hex_list = parse_hex(ra_string)
    try:
        if len(hex_list) == 1:
            return None  # input in degrees NOT allowed here.
        elif len(hex_list) == 2:
            if (int(hex_list[1]) >= 60) or (int(hex_list[1]) < 0):
                return None
            ra_degrees = 15 * (int(hex_list[0]) + int(hex_list[1])/60.0)  # input assumed in hex.
        else:
            if (int(hex_list[1]) >= 60) or (int(hex_list[1]) < 0) or\
               (float(hex_list[2]) >= 60) or (float(hex_list[2]) < 0):
                return None
            ra_degrees = 15 * (int(hex_list[0]) + int(hex_list[1]) / 60.0 +
                               float(hex_list[2])/3600.0)  # input assumed in hex.
    except ValueError:
        return None
    if (ra_degrees < 0) or (ra_degrees > 360):
        return None
    return ra_degrees


def dec_as_degrees(dec_text):
    return latitude_as_degrees(dec_text)  # exactly the same math & limits.


RECAST_TO_TEXT___________________ = 0


def ra_as_hours(ra_degrees):
    """ Input: float of Right Ascension in degrees.
        Returns: string of RA as hours, in hex, to the nearest 0.001 RA seconds.
     from photrix August 2018.
   """
    if (ra_degrees < 0) | (ra_degrees > 360):
        return None
    n_ra_milliseconds = round((ra_degrees * 3600 * 1000) / 15)
    ra_hours, remainder = divmod(n_ra_milliseconds, 3600 * 1000)
    ra_minutes, remainder = divmod(remainder, 60 * 1000)
    ra_seconds = round(remainder / 1000, 3)
    format_string = "{0:02d}:{1:02d}:{2:06.3f}"
    ra_str = format_string.format(int(ra_hours), int(ra_minutes), ra_seconds)
    if ra_str[:3] == "24:":
        ra_str = format_string.format(0, 0, 0)
    return ra_str


def degrees_as_hex(angle_degrees, seconds_decimal_places=2):
    """
    :param angle_degrees: any angle as degrees [float]
    :param seconds_decimal_places: number of decimal places to express for seconds part of hex string [int]
    :return: same angle in hex notation, unbounded [string].
    from photrix August 2018.
    """
    if angle_degrees < 0:
        sign = "-"
    else:
        sign = "+"
    abs_degrees = abs(angle_degrees)
    milliseconds = round(abs_degrees * 3600 * 1000)
    degrees, remainder = divmod(milliseconds, 3600 * 1000)
    minutes, remainder = divmod(remainder, 60 * 1000)
    seconds = round(remainder / 1000, 2)
    format_string = '{0}{1:02d}:{2:02d}:{3:0' + str(int(seconds_decimal_places)+3) + \
                    '.0' + str(int(seconds_decimal_places)) + 'f}'
    hex_string = format_string.format(sign, int(degrees), int(minutes), seconds)
    return hex_string


def datetime_as_string(this_datetime):
    if not isinstance(this_datetime, datetime):
        return None
    return '{:%Y-%m-%d %H:%M:%S}  UTC'.format(this_datetime)
