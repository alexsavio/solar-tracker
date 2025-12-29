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

    def estimate_monthly_energy(
        self,
        month: int,
        area_m2: float = 1.0,
        efficiency: float = 0.2,
        dni: float = 1000.0,
        time_step_hours: float = 1.0,
    ) -> float:
        """
        Estimate monthly solar energy production for the panel using a simple model.

        This uses an hourly integration over every day in the given month. For each
        timestep it computes the sun position using a simple solar geometry model
        (declination + hour angle), computes the angle between the sun vector and
        the panel normal, and accumulates the direct-beam contribution using the
        provided direct normal irradiance (`dni`). The result is returned in
        kilowatt-hours (kWh) for the whole month for the given panel area and
        conversion efficiency.

        Notes / assumptions:
        - Uses a simple declination model (no equation-of-time corrections).
        - Uses hourly (or coarse) timesteps; smaller `time_step_hours` increases accuracy.
        - Only direct normal irradiance is considered (no diffuse or ground-reflected).

        Args:
            month: Month number (1-12).
            area_m2: Panel area in square meters.
            efficiency: Panel conversion efficiency (0-1).
            dni: Direct normal irradiance in W/m^2 when sun is normal to surface.
            time_step_hours: Integration timestep in hours.

        Returns:
            float: Estimated energy for the month in kWh.
        """
        # Days in each month (non-leap year)
        month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if not (1 <= month <= 12):
            raise ValueError("month must be in 1..12")

        days = month_days[month - 1]

        # Helper: day of year for given month/day (1-indexed)
        cumulative_days = [0]
        for d in month_days:
            cumulative_days.append(cumulative_days[-1] + d)

        total_wh = 0.0

        phi = math.radians(self.latitude)
        panel_tilt_rad = math.radians(self.tilt)
        # Panel azimuth to azimuth-from-north (radians). Input azimuth: 0=South, +West, -East
        panel_az_north_rad = math.radians(180.0 + self.azimuth)

        sin_panel_tilt = math.sin(panel_tilt_rad)
        cos_panel_tilt = math.cos(panel_tilt_rad)

        # Loop over days and timesteps
        for day in range(1, days + 1):
            n = cumulative_days[month - 1] + day  # day of year

            # solar declination (radians)
            decl = math.radians(23.45) * math.sin(2 * math.pi * (284 + n) / 365)

            t = 0.0
            while t < 24.0:
                # approximate local solar time from longitude: solar_time = clock_time + longitude/15
                solar_time = t + (self.longitude / 15.0)
                hour_angle = math.radians(15.0 * (solar_time - 12.0))

                # solar elevation: sin(alpha) = sin(phi)*sin(delta) + cos(phi)*cos(delta)*cos(omega)
                sin_alpha = math.sin(phi) * math.sin(decl) + math.cos(phi) * math.cos(
                    decl
                ) * math.cos(hour_angle)

                if sin_alpha > 0:
                    # solar zenith and cos(alpha)
                    cos_alpha = math.sqrt(max(0.0, 1.0 - sin_alpha * sin_alpha))

                    # solar azimuth components (from north)
                    # sinA = (cosδ * sinω) / cosα
                    # cosA = (sinδ * cosφ - cosδ * sinφ * cosω) / cosα
                    # guard against division by zero
                    if cos_alpha > 1e-8:
                        sinA = (math.cos(decl) * math.sin(hour_angle)) / cos_alpha
                        cosA = (
                            math.sin(decl) * math.cos(phi)
                            - math.cos(decl) * math.sin(phi) * math.cos(hour_angle)
                        ) / cos_alpha
                    else:
                        sinA = 0.0
                        cosA = 1.0

                    az_north = math.atan2(sinA, cosA)
                    # normalize to 0..2pi
                    if az_north < 0:
                        az_north += 2 * math.pi

                    # Sun unit vector in local coords (x=east, y=north, z=up)
                    sun_x = cos_alpha * math.sin(az_north)
                    sun_y = cos_alpha * math.cos(az_north)
                    sun_z = sin_alpha

                    # Panel normal unit vector
                    n_x = sin_panel_tilt * math.sin(panel_az_north_rad)
                    n_y = sin_panel_tilt * math.cos(panel_az_north_rad)
                    n_z = cos_panel_tilt

                    dot = sun_x * n_x + sun_y * n_y + sun_z * n_z

                    if dot > 0:
                        power_w = dni * dot * area_m2 * efficiency
                        total_wh += power_w * time_step_hours

                t += time_step_hours

        # convert Wh to kWh
        return total_wh / 1000.0
