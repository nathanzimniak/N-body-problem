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
    #M_jupiter = 9.55e-4
    #M_saturn  = 2.86e-4
    #M_uranus  = 4.37e-5
    #M_neptune = 5.15e-5
    masses = [M_sun,
              M_mercury,
              M_venus,
              M_earth,
              M_mars]#,
              #M_jupiter,
              #M_saturn,
              #M_uranus,
              #M_neptune]

    # Semi-major axes (in AU)
    a_mercury = 0.39
    a_venus   = 0.723
    a_earth   = 1.0
    a_mars    = 1.524
    #a_jupiter = 5.204
    #a_saturn  = 9.58
    #a_uranus  = 19.2
    #a_neptune = 30.1
    positions = [[0.0, 0.0, 0.0],
                 [a_mercury, 0.0, 0.0],
                 [a_venus,   0.0, 0.0],
                 [a_earth,   0.0, 0.0],
                 [a_mars,    0.0, 0.0]]#,
                 #[a_jupiter, 0.0, 0.0],
                 #[a_saturn,  0.0, 0.0],
                 #[a_uranus,  0.0, 0.0],
                 #[a_neptune, 0.0, 0.0]]

    # Velocities for circular orbits (in AU/year)
    v_mercury = 2*math.pi/math.sqrt(a_mercury)
    v_venus   = 2*math.pi/math.sqrt(a_venus)
    v_earth   = 2*math.pi/math.sqrt(a_earth)
    v_mars    = 2*math.pi/math.sqrt(a_mars)
    #v_jupiter = 2*math.pi/math.sqrt(a_jupiter)
    #v_saturn  = 2*math.pi/math.sqrt(a_saturn)
    #v_uranus  = 2*math.pi/math.sqrt(a_uranus)
    #v_neptune = 2*math.pi/math.sqrt(a_neptune)
    velocities = [[0.0, 0.0, 0.0],
                  [0.0,  v_mercury, 0.0],
                  [0.0,  v_venus, 0.0],
                  [0.0,  v_earth, 0.0],
                  [0.0,  v_mars, 0.0]]#,
                  #[0.0,  v_jupiter, 0.0],
                  #[0.0,  v_saturn, 0.0],
                  #[0.0,  v_uranus, 0.0],
                  #[0.0,  v_neptune, 0.0]]

    trail_length      = 50
    point_colors      = ["#FFB81F", "#6E6D88", "#C39531", "#006FFF", "#FF2F00"]
    point_edge_colors = ["#FFB81F", "#6E6D88", "#C39531", "#006FFF", "#FF2F00"]
    trail_colors      = ["#FFB81F", "#6E6D88", "#C39531", "#006FFF", "#FF2F00"]
    point_sizes       = [13, 3, 5, 6, 4]
    point_edge_widths = [15/5, 3/5, 5/5, 6/5, 4/5]
    trail_widths      = [15/3, 3/3, 5/3, 6/3, 4/3]
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

def outer_solar_system():
    # Time parameters
    t_ini   = 0.0
    t_end   = 50.0           # Simulate 50 years
    N_steps = int(36.5*t_end) # 1 step per 10 days

    # Masses (in solar masses)
    M_sun     = 1.0
    M_jupiter = 9.55e-4
    M_saturn  = 2.86e-4
    M_uranus  = 4.37e-5
    M_neptune = 5.15e-5
    masses = [M_sun,
              M_jupiter,
              M_saturn,
              M_uranus,
              M_neptune]

    # Semi-major axes (in AU)
    a_jupiter = 5.204
    a_saturn  = 9.58
    a_uranus  = 19.2
    a_neptune = 30.1
    positions = [[0.0, 0.0, 0.0],
                 [a_jupiter, 0.0, 0.0],
                 [a_saturn,  0.0, 0.0],
                 [a_uranus,  0.0, 0.0],
                 [a_neptune, 0.0, 0.0]]

    # Velocities for circular orbits (in AU/year)
    v_jupiter = 2*math.pi/math.sqrt(a_jupiter)
    v_saturn  = 2*math.pi/math.sqrt(a_saturn)
    v_uranus  = 2*math.pi/math.sqrt(a_uranus)
    v_neptune = 2*math.pi/math.sqrt(a_neptune)
    velocities = [[0.0, 0.0, 0.0],
                  [0.0,  v_jupiter, 0.0],
                  [0.0,  v_saturn, 0.0],
                  [0.0,  v_uranus, 0.0],
                  [0.0,  v_neptune, 0.0]]

    trail_length      = 50
    point_colors      = ["#FFB81F", "#6E6D88", "#C39531", "#006FFF", "#FF2F00"]
    point_edge_colors = ["#FFB81F", "#6E6D88", "#C39531", "#006FFF", "#FF2F00"]
    trail_colors      = ["#FFB81F", "#6E6D88", "#C39531", "#006FFF", "#FF2F00"]
    point_sizes       = [13, 3, 5, 6, 4]
    point_edge_widths = [15/5, 3/5, 5/5, 6/5, 4/5]
    trail_widths      = [15/3, 3/3, 5/3, 6/3, 4/3]
    axis_limits       = [-30.0, 30.0, -30.0, 30.0, -30.0, 30.0]
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
                     "inner_solar_system": inner_solar_system,
                     "outer_solar_system": outer_solar_system}


def load_preset(name="default"):
    if name not in AVAILABLE_PRESETS: raise ValueError(f"Preset '{name}' unknown. Available presets: {list(AVAILABLE_PRESETS)}")
    return AVAILABLE_PRESETS[name]()
