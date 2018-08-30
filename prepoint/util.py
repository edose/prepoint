from datetime import datetime, timezone
import math

import ephem

__author__ = "Eric Dose :: New Mexico Mira Project, Albuquerque"


def jd_from_datetime_utc(datetime_utc=None):
    """  Converts a UTC datetime to Julian date. Imported from photrix (E. Dose).
    :param datetime_utc: date and time (in UTC) to convert [python datetime object]
    :return: Julian date corresponding to date and time [float].
    from photrix August 2018.
    """
    if datetime_utc is None:
        return None
    datetime_j2000 = datetime(2000, 1, 1, 0, 0, 0).replace(tzinfo=timezone.utc)
    jd_j2000 = 2451544.5
    seconds_since_j2000 = (datetime_utc - datetime_j2000).total_seconds()
    return jd_j2000 + seconds_since_j2000 / (24*3600)


def jd_now():
    """  Returns Julian date of moment this function is called. Imported from photrix (E. Dose).
    :return: Julian date for immediate present per system clock [float].
    from photrix August 2018.
    """
    return jd_from_datetime_utc(datetime.now(timezone.utc))


def calc_az_alt(ra, dec, longitude, latitude, datetime_utc):
    """  Returns azimuth and altitude for sky position (RA and Dec)
         at a given earth longitude and Latitude, at a given date and time (in UTC).
    :param ra: right ascension of sky position, in degrees [float].
    :param dec: declination of sky position, in degrees [float].
    :param longitude: longitude of earth position, in degrees east=positive [float].
    :param latitude: latitude of earth position, in degrees north=positive [float].
    :param datetime_utc: date and time for which to calculate az and alt, in UTC [datetime object].
    :return: 2-tuple of azimuth, altitude in degrees [2-tuple of floats].
    adapted from photrix August 2018.
    """
    # TODO: recast this fn for separate ra, dec, rather than RaDec object.
    obs = ephem.Observer()  # for local use.
    obs.lon = str(longitude * math.pi / 180)  # cast to radians then to string.
    obs.lat = str(latitude * math.pi / 180)   # "
    obs.date = datetime_utc

    target_ephem = ephem.FixedBody()  # so named to suggest restricting its use to ephem.
    target_ephem._epoch = '2000'
    target_ephem._ra = ra_as_hours(ra)
    target_ephem._dec = degrees_as_hex(dec)
    target_ephem.compute(obs)
    return target_ephem.az * 180 / math.pi, target_ephem.alt * 180 / math.pi


PARSE_TEXT_TO_DEGREES___________________ = 0


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
    adapted from photrix.util August 2018; added return=None for unparseable string.
    """
    # dec_list = hex_degrees_string.split(":")
    dec_list = parse_hex(hex_degrees_string)
    # dec_list = [dec.strip() for dec in dec_list]
    if dec_list[0].startswith("-"):
        sign = -1
    else:
        sign = 1
    try:
        if len(dec_list) == 1:
            dec_degrees = float(dec_list[0])  # input assumed to be in degrees.
        elif len(dec_list) == 2:
            dec_degrees = sign * (abs(float(dec_list[0])) + float(dec_list[1])/60.0)  # input is hex.
        else:
            dec_degrees = sign * (abs(float(dec_list[0])) + float(dec_list[1]) / 60.0 +
                                  float(dec_list[2])/3600.0)  # input is hex.
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
    :param ra_string: string in either full hex ("12:34:56.7777" or "12 34 56.7777"),
               or degrees ("234.55")
    :return float of Right Ascension in degrees between 0 and 360.
    adapted from photrix.util August 2018; added return=None for unparseable string.
    """
    ra_list = parse_hex(ra_string)
    try:
        if len(ra_list) == 1:
            ra_degrees = float(ra_list[0])  # input assumed to be in degrees.
        elif len(ra_list) == 2:
            ra_degrees = 15 * (float(ra_list[0]) + float(ra_list[1])/60.0)  # input assumed in hex.
        else:
            ra_degrees = 15 * (float(ra_list[0]) + float(ra_list[1]) / 60.0 +
                               float(ra_list[2])/3600.0)  # input assumed in hex.
    except ValueError:
        return None
    if (ra_degrees < 0) | (ra_degrees > 360):
        ra_degrees = None
    return ra_degrees


def dec_as_degrees(dec_text):
    return latitude_as_degrees(dec_text)  # exactly the same math & limits.


RECAST_TO_STRING___________________ = 0


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
    :param angle_degrees: any angle as degrees
    :return: same angle in hex notation, unbounded.
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

 
# def dec_as_hex(dec_degrees):
#     """ Input: float of Declination in degrees.
#         Returns: string of Declination in hex, to the nearest 0.01 arcsecond.
#     from photrix August 2018.
#     """
#     if (dec_degrees < -90) | (dec_degrees > +90):
#         return None
#     dec_string = degrees_as_hex(dec_degrees, seconds_decimal_places=2)
#     return dec_string
