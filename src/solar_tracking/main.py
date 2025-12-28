"""Solar Tracking Calculations"""

from __future__ import annotations

import math


def calculate_declination(day_of_year: int) -> float:
    """
    Calculate the solar declination angle in degrees.

    Args:
        day_of_year (int): The day of the year (1-365).

    Returns:
        float: The declination angle in degrees.
    """
    # Cooper's equation
    return 23.45 * math.sin(math.radians(360 * (284 + day_of_year) / 365))


def calculate_elevation(
    latitude: float, declination: float, hour_angle: float
) -> float:
    """
    Calculate the solar elevation angle (altitude) in degrees.

    Args:
        latitude (float): The latitude of the observer in degrees.
        declination (float): The solar declination angle in degrees.
        hour_angle (float): The solar hour angle in degrees.

    Returns:
        float: The solar elevation angle in degrees.
    """
    latitude_radians = math.radians(latitude)
    declination_radians = math.radians(declination)
    hour_angle_radians = math.radians(hour_angle)

    sin_elevation = math.sin(latitude_radians) * math.sin(
        declination_radians
    ) + math.cos(latitude_radians) * math.cos(declination_radians) * math.cos(
        hour_angle_radians
    )

    # Clamp value to [-1, 1] to handle floating point errors
    sin_elevation = max(-1.0, min(1.0, sin_elevation))

    return math.degrees(math.asin(sin_elevation))


def calculate_azimuth(
    latitude: float, declination: float, hour_angle: float, elevation: float
) -> float:
    """
    Calculate the solar azimuth angle in degrees.

    Args:
        latitude (float): The latitude of the observer in degrees.
        declination (float): The solar declination angle in degrees.
        hour_angle (float): The solar hour angle in degrees.
        elevation (float): The solar elevation angle in degrees.

    Returns:
        float: The solar azimuth angle in degrees.
    """
    latitude_radians = math.radians(latitude)
    declination_radians = math.radians(declination)
    elevation_radians = math.radians(elevation)

    # Avoid division by zero at zenith
    if abs(90 - abs(elevation)) < 1e-6:
        return 0.0

    cos_azimuth = (
        math.sin(declination_radians) * math.cos(latitude_radians)
        - math.cos(declination_radians)
        * math.sin(latitude_radians)
        * math.cos(math.radians(hour_angle))
    ) / math.cos(elevation_radians)

    # Clamp value to [-1, 1]
    cos_azimuth = max(-1.0, min(1.0, cos_azimuth))

    azimuth = math.degrees(math.acos(cos_azimuth))

    # Adjust azimuth based on hour angle (afternoon vs morning)
    # Convention: 0 is South, East is negative, West is positive (or similar depending on convention)
    # Here we return 0 to 360 or -180 to 180.
    # Usually: if hour_angle > 0 (afternoon), azimuth is positive (West).
    # If hour_angle < 0 (morning), azimuth is negative (East).
    # The acos returns 0 to 180.

    if hour_angle > 0:
        return azimuth
    else:
        return -azimuth


def calculate_equation_of_time(day_of_year: int) -> float:
    """
    Calculate the Equation of Time (EoT) in minutes.

    Args:
        day_of_year (int): The day of the year (1-365).

    Returns:
        float: The Equation of Time in minutes.
    """
    day_angle = 360 * (day_of_year - 81) / 365
    day_angle_radians = math.radians(day_angle)

    equation_of_time = (
        9.87 * math.sin(2 * day_angle_radians)
        - 7.53 * math.cos(day_angle_radians)
        - 1.5 * math.sin(day_angle_radians)
    )
    return equation_of_time


def calculate_sunrise_sunset(
    latitude: float, longitude: float, day_of_year: int
) -> tuple[float | None, float | None]:
    """
    Calculate the sunrise and sunset times in UTC hours.

    Args:
        latitude (float): The latitude of the observer in degrees.
        longitude (float): The longitude of the observer in degrees (East is positive).
        day_of_year (int): The day of the year (1-365).

    Returns:
        tuple[float | None, float | None]: Sunrise and sunset times in UTC hours.
                             Returns (None, None) if sun does not rise or set.
    """
    declination = calculate_declination(day_of_year)

    latitude_radians = math.radians(latitude)
    declination_radians = math.radians(declination)

    # Calculate hour angle for sunrise/sunset
    # cos(omega) = -tan(phi) * tan(delta)
    # Check for division by zero or invalid tan if latitude is 90
    if abs(abs(latitude) - 90) < 1e-6:
        # At poles, it's either polar day or night depending on declination
        if latitude * declination > 0:
            return None, None  # Polar day
        else:
            return None, None  # Polar night

    tan_latitude = math.tan(latitude_radians)
    tan_declination = math.tan(declination_radians)
    cos_hour_angle = -tan_latitude * tan_declination

    # Check for polar day/night
    if cos_hour_angle > 1.0:
        return None, None  # Sun never rises (Polar Night)
    if cos_hour_angle < -1.0:
        return None, None  # Sun never sets (Polar Day)

    hour_angle_degrees = math.degrees(math.acos(cos_hour_angle))

    # Solar noon in UTC
    equation_of_time = calculate_equation_of_time(day_of_year)
    solar_noon_utc = 12.0 - (longitude / 15.0) - (equation_of_time / 60.0)

    # Sunrise and Sunset
    sunrise_utc = solar_noon_utc - (hour_angle_degrees / 15.0)
    sunset_utc = solar_noon_utc + (hour_angle_degrees / 15.0)

    # Normalize to 0-24 range
    sunrise_utc = sunrise_utc % 24
    sunset_utc = sunset_utc % 24

    return sunrise_utc, sunset_utc


def main():
    # Example usage
    latitude = 40.7128  # New York
    day_of_year = 172  # Summer Solstice
    hour_angle = -15  # 11:00 AM Solar Time

    declination = calculate_declination(day_of_year)
    elevation = calculate_elevation(latitude, declination, hour_angle)
    azimuth = calculate_azimuth(latitude, declination, hour_angle, elevation)

    print(f"Latitude: {latitude}°")
    print(f"Day of Year: {day_of_year}")
    print(f"Hour Angle: {hour_angle}°")
    print("-" * 20)
    print(f"Declination: {declination:.2f}°")
    print(f"Elevation: {elevation:.2f}°")
    print(f"Azimuth: {azimuth:.2f}°")

    longitude = -74.0060  # New York
    sunrise, sunset = calculate_sunrise_sunset(latitude, longitude, day_of_year)
    print("-" * 20)
    if sunrise is not None:
        print(f"Sunrise (UTC): {sunrise:.2f} h")
        print(f"Sunset (UTC): {sunset:.2f} h")
    else:
        print("Polar day or night (no sunrise/sunset)")


if __name__ == "__main__":
    main()
