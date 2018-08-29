from datetime import datetime, timezone
import math

import ephem

__author__ = "Eric Dose :: New Mexico Mira Project, Albuquerque"


def jd_from_datetime_utc(datetime_utc=None):
    """  Converts a UTC datetime to Julian date. Imported from photrix (E. Dose).
    :param datetime_utc: date and time (in UTC) to convert [python datetime object]
    :return: Julian date corresponding to date and time [float].
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
    """
    return jd_from_datetime_utc(datetime.now(timezone.utc))


def calc_az_alt(ra, dec, longitude, latitude, datetime_utc):
#
# def az_alt_at_datetime_utc(longitude, latitude, target_radec, datetime_utc):
    obs = ephem.Observer()  # for local use.
    obs.lon = str(longitude * math.pi / 180)  # cast to radians then to string.
    obs.lat = str(latitude * math.pi / 180)   # "
    obs.date = datetime_utc

    target_ephem = ephem.FixedBody()  # so named to suggest restricting its use to ephem.
    target_ephem._epoch = '2000'
    this_ra = ra_as_degrees(ra)

    target_ephem._ra, target_ephem._dec = target_radec.as_hex  # text: RA in hours, Dec in deg
    target_ephem.compute(obs)
    return target_ephem.az * 180 / math.pi, target_ephem.alt * 180 / math.pi
