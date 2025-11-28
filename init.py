import math

def earth_sun():
    # Time parameters
    t_ini   = 0.0
    t_end   = 1.0            # Simulate 1 year
    N_steps = int(365*t_end) # 1 step per day

    # Masses (in solar masses)
    M_sun     = 1.0
    M_earth   = 3.00e-6
    masses = [M_sun,
              M_earth]

    # Semi-major axes (in AU)
    a_earth   = 1.0
    positions = [[0.0, 0.0, 0.0],
                 [a_earth, 0.0, 0.0]]

    # Velocities for circular orbits (in AU/year)
    v_earth   = 2*math.pi/math.sqrt(a_earth)
    velocities = [[0.0, 0.0, 0.0],
                  [0.0,  v_earth, 0.0]]

    trail_length      = 50
    point_colors      = ["#FFB81F", "#006FFF"]
    point_edge_colors = ["#FFB81F", "#006FFF"]
    trail_colors      = ["#FFB81F", "#006FFF"]
    point_sizes       = [13, 6]
    point_edge_widths = [15/5, 6/5]
    trail_widths      = [15/3, 6/3]
    axis_limits       = [-2.0, 2.0, -2.0, 2.0, -2.0, 2.0]
    elevation_angle   = 35
    azimuthal_angle   = 45

    return {"t_ini":             t_ini,
            "t_end":             t_end,
            "N_steps":           N_steps,
            "masses":            masses,
            "positions":         positions,
            "velocities":        velocities,
            "trail_length":      trail_length,
            "point_colors":      point_colors,
            "point_edge_colors": point_edge_colors,
            "trail_colors":      trail_colors,
            "point_sizes":       point_sizes,
            "point_edge_widths": point_edge_widths,
            "trail_widths":      trail_widths,
            "axis_limits":       axis_limits,
            "elevation_angle":   elevation_angle,
            "azimuthal_angle":   azimuthal_angle}


def inner_solar_system():
    # Time parameters
    t_ini   = 0.0
    t_end   = 50.0           # Simulate 50 years
    N_steps = int(365*t_end) # 1 step per 1 days

    # Masses (in solar masses)
    M_sun     = 1.0
    M_mercury = 1.65e-7
    M_venus   = 2.45e-6
    M_earth   = 3.00e-6
    M_mars    = 3.23e-7
    masses = [M_sun,
              M_mercury,
              M_venus,
              M_earth,
              M_mars]

    # Semi-major axes (in AU)
    a_mercury = 0.39
    a_venus   = 0.723
    a_earth   = 1.0
    a_mars    = 1.524
    positions = [[0.0, 0.0, 0.0],
                 [a_mercury, 0.0, 0.0],
                 [a_venus,   0.0, 0.0],
                 [a_earth,   0.0, 0.0],
                 [a_mars,    0.0, 0.0]]

    # Velocities for circular orbits (in AU/year)
    v_mercury = 2*math.pi/math.sqrt(a_mercury)
    v_venus   = 2*math.pi/math.sqrt(a_venus)
    v_earth   = 2*math.pi/math.sqrt(a_earth)
    v_mars    = 2*math.pi/math.sqrt(a_mars)
    velocities = [[0.0, 0.0, 0.0],
                  [0.0,  v_mercury, 0.0],
                  [0.0,  v_venus, 0.0],
                  [0.0,  v_earth, 0.0],
                  [0.0,  v_mars, 0.0]]

    trail_length      = 50
    point_colors      = ["#FFB81F", "#6E6D88", "#C39531", "#006FFF", "#FF2F00"]
    point_edge_colors = ["#FFB81F", "#6E6D88", "#C39531", "#006FFF", "#FF2F00"]
    trail_colors      = ["#FFB81F", "#6E6D88", "#C39531", "#006FFF", "#FF2F00"]
    point_sizes       = [13, 3, 5, 6, 4]
    point_edge_widths = [size/5 for size in point_sizes]
    trail_widths      = [size/3 for size in point_sizes]
    axis_limits       = [-2.0, 2.0, -2.0, 2.0, -2.0, 2.0]
    elevation_angle   = 35
    azimuthal_angle   = 45

    return {"t_ini":             t_ini,
            "t_end":             t_end,
            "N_steps":           N_steps,
            "masses":            masses,
            "positions":         positions,
            "velocities":        velocities,
            "trail_length":      trail_length,
            "point_colors":      point_colors,
            "point_edge_colors": point_edge_colors,
            "trail_colors":      trail_colors,
            "point_sizes":       point_sizes,
            "point_edge_widths": point_edge_widths,
            "trail_widths":      trail_widths,
            "axis_limits":       axis_limits,
            "elevation_angle":   elevation_angle,
            "azimuthal_angle":   azimuthal_angle}

# ----- Sélecteur de preset -----

AVAILABLE_PRESETS = {"earth_sun": earth_sun,
                     "inner_solar_system": inner_solar_system}


def load_preset(name="default"):
    if name not in AVAILABLE_PRESETS: raise ValueError(f"Preset '{name}' unknown. Available presets: {list(AVAILABLE_PRESETS)}")
    return AVAILABLE_PRESETS[name]()
