import math

from solar_tracking.solar_panel import SolarPanel


def test_solar_panel_initialization():
    panel = SolarPanel(latitude=40.0, longitude=-74.0, azimuth=0.0, tilt=30.0)
    assert panel.latitude == 40.0
    assert panel.longitude == -74.0
    assert panel.azimuth == 0.0
    assert panel.tilt == 30.0


def test_incidence_angle_perpendicular():
    # If panel is facing South (0) with tilt 30
    # And sun is South (0) with elevation 60 (zenith 30)
    # Then incidence should be 0 (perpendicular)
    # Because 90 - 60 = 30 degrees zenith, which matches the tilt

    panel = SolarPanel(latitude=40.0, longitude=0.0, azimuth=0.0, tilt=30.0)
    incidence = panel.calculate_incidence_angle(sun_azimuth=0.0, sun_elevation=60.0)

    assert math.isclose(incidence, 0.0, abs_tol=1e-5)


def test_incidence_angle_flat_panel():
    # Flat panel (tilt 0)
    # Sun at zenith (elevation 90)
    # Incidence should be 0

    panel = SolarPanel(latitude=0.0, longitude=0.0, azimuth=0.0, tilt=0.0)
    incidence = panel.calculate_incidence_angle(sun_azimuth=123.0, sun_elevation=90.0)

    assert math.isclose(incidence, 0.0, abs_tol=1e-5)


def test_incidence_angle_vertical_panel():
    # Vertical panel facing South (tilt 90, azimuth 0)
    # Sun at South horizon (elevation 0, azimuth 0)
    # Incidence should be 0

    panel = SolarPanel(latitude=0.0, longitude=0.0, azimuth=0.0, tilt=90.0)
    incidence = panel.calculate_incidence_angle(sun_azimuth=0.0, sun_elevation=0.0)

    assert math.isclose(incidence, 0.0, abs_tol=1e-5)

    # Sun at North horizon (elevation 0, azimuth 180)
    # Incidence should be 180 (back of panel)
    incidence_back = panel.calculate_incidence_angle(
        sun_azimuth=180.0, sun_elevation=0.0
    )
    assert math.isclose(incidence_back, 180.0, abs_tol=1e-5)
