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

    return {"t_ini":             t_ini,
            "t_end":             t_end,
            "N_steps":           N_steps,
            "masses":            masses,
            "positions":         positions,
            "velocities":        velocities}


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
    masses    = [M_sun,
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
    v_mercury  = 2*math.pi/math.sqrt(a_mercury)
    v_venus    = 2*math.pi/math.sqrt(a_venus)
    v_earth    = 2*math.pi/math.sqrt(a_earth)
    v_mars     = 2*math.pi/math.sqrt(a_mars)
    velocities = [[0.0, 0.0, 0.0],
                  [0.0,  v_mercury, 0.0],
                  [0.0,  v_venus, 0.0],
                  [0.0,  v_earth, 0.0],
                  [0.0,  v_mars, 0.0]]

    return {"t_ini":             t_ini,
            "t_end":             t_end,
            "N_steps":           N_steps,
            "masses":            masses,
            "positions":         positions,
            "velocities":        velocities}

def three_body_3d_orbits():
    # Time parameters
    t_ini   = 0.0
    t_end   = 20.0           # durée suffisante pour voir plusieurs périodes
    N_steps = int(2000)      # à adapter si tu veux plus/moins de résolution

    # Masses (toutes égales, unités arbitraires cohérentes)
    M1 = 1.0
    M2 = 1.0
    M3 = 1.0
    masses = [M1, M2, M3]

    # Positions initiales (tes x, avec z = 0)
    x1, y1, z1 = -1.0, 0.0, 0.0
    x2, y2, z2 =  1.0, 0.0, 0.0
    x3, y3, z3 =  0.0, 0.0, 0.0
    positions = [[x1, y1, z1],
                 [x2, y2, z2],
                 [x3, y3, z3]]

    # Vitesses initiales (tes v, avec vz = 0)
    vx1, vy1, vz1 = 0.464445,  0.39606, 0.0
    vx2, vy2, vz2 = 0.464445,  0.39606, 0.0
    vx3, vy3, vz3 = -0.92889,  -0.79212, 0.0
    velocities = [[vx1, vy1, vz1],
                  [vx2, vy2, vz2],
                  [vx3, vy3, vz3]]

    return {"t_ini":             t_ini,
            "t_end":             t_end,
            "N_steps":           N_steps,
            "masses":            masses,
            "positions":         positions,
            "velocities":        velocities}







# ----- Sélecteur de preset -----

AVAILABLE_PRESETS = {"earth_sun": earth_sun,
                     "inner_solar_system": inner_solar_system,
                     "three_body_3d_orbits": three_body_3d_orbits}


def load_preset(name="default"):
    if name not in AVAILABLE_PRESETS: raise ValueError(f"Preset '{name}' unknown. Available presets: {list(AVAILABLE_PRESETS)}")
    return AVAILABLE_PRESETS[name]()
