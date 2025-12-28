import math

from solar_tracking.main import (
    calculate_azimuth,
    calculate_declination,
    calculate_elevation,
    calculate_equation_of_time,
    calculate_sunrise_sunset,
)


def test_calculate_declination():
    # Equinox (approx day 80) should be near 0
    declination = calculate_declination(80)
    assert math.isclose(declination, 0, abs_tol=2.0)

    # Summer Solstice (approx day 172) should be near 23.45
    declination = calculate_declination(172)
    assert math.isclose(declination, 23.45, abs_tol=0.5)


def test_calculate_elevation():
    # At equator, equinox, noon (hour angle 0) -> elevation 90
    elevation = calculate_elevation(0, 0, 0)
    assert math.isclose(elevation, 90, abs_tol=0.1)


def test_calculate_azimuth():
    # At equator, equinox, morning (-90 hour angle) -> azimuth -90 (East)
    # Elevation would be 0
    azimuth = calculate_azimuth(0, 0, -90, 0)
    assert math.isclose(azimuth, -90, abs_tol=0.1)


def test_calculate_equation_of_time():
    # EoT is roughly between -17 and +17 minutes
    for day in range(1, 366):
        eot = calculate_equation_of_time(day)
        assert -17 <= eot <= 17


def test_calculate_sunrise_sunset_equator_equinox():
    # Equator (0 lat), Prime Meridian (0 lon), Equinox (~day 80)
    # Sunrise should be approx 6:00 UTC, Sunset approx 18:00 UTC
    sunrise, sunset = calculate_sunrise_sunset(0, 0, 80)

    # Allow some margin because day 80 is approx equinox and EoT
    assert math.isclose(sunrise, 6.0, abs_tol=0.5)
    assert math.isclose(sunset, 18.0, abs_tol=0.5)


def test_calculate_sunrise_sunset_polar_night():
    # North Pole in winter (e.g., day 355)
    sunrise, sunset = calculate_sunrise_sunset(90, 0, 355)
    assert sunrise is None
    assert sunset is None


def test_calculate_sunrise_sunset_polar_day():
    # North Pole in summer (e.g., day 172)
    sunrise, sunset = calculate_sunrise_sunset(90, 0, 172)
    assert sunrise is None
    assert sunset is None
