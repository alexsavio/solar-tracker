"""Module defining the SolarPanel class for solar tracking applications."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class SolarPanel:
    """
    Represents a solar panel at a specific geographical location and orientation.

    Attributes:
        latitude (float): Latitude of the location in degrees.
        longitude (float): Longitude of the location in degrees.
        azimuth (float): Orientation of the panel in degrees (0 = South, negative East, positive West).
        tilt (float): Inclination of the panel from horizontal in degrees (0 = flat, 90 = vertical).
    """

    latitude: float
    longitude: float
    azimuth: float
    tilt: float

    def calculate_incidence_angle(
        self, sun_azimuth: float, sun_elevation: float
    ) -> float:
        """
        Calculates the angle of incidence of sunlight on the panel.

        The angle of incidence is the angle between the sun's rays and the normal to the panel surface.
        0 degrees means the sun is directly perpendicular to the panel (maximum efficiency).

        Args:
            sun_azimuth (float): Solar azimuth in degrees.
            sun_elevation (float): Solar elevation in degrees.

        Returns:
            float: Angle of incidence in degrees.
        """
        # Convert inputs to radians
        tilt_rad = math.radians(self.tilt)
        panel_az_rad = math.radians(self.azimuth)
        sun_az_rad = math.radians(sun_azimuth)

        # Zenith angle is 90 - elevation
        sun_zenith_rad = math.radians(90 - sun_elevation)

        # Formula for incidence angle theta:
        # cos(theta) = cos(sun_zenith) * cos(panel_tilt) +
        #              sin(sun_zenith) * sin(panel_tilt) * cos(sun_azimuth - panel_azimuth)

        cos_theta = math.cos(sun_zenith_rad) * math.cos(tilt_rad) + math.sin(
            sun_zenith_rad
        ) * math.sin(tilt_rad) * math.cos(sun_az_rad - panel_az_rad)

        # Clamp value to [-1, 1] to handle floating point errors
        cos_theta = max(-1.0, min(1.0, cos_theta))

        return math.degrees(math.acos(cos_theta))
