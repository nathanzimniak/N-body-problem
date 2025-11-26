import math

def earth_sun():
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

    return {"t_ini":      t_ini,
            "t_end":      t_end,
            "N_steps":    N_steps,
            "masses":     masses,
            "positions":  positions,
            "velocities": velocities}


def solar_system():
    t_ini   = 0.0
    t_end   = 50.0           # Simulate 50 years
    N_steps = int(365*t_end) # 1 step per 1 days

    # Masses (in solar masses)
    M_sun     = 1.0
    M_mercury = 1.65e-7
    M_venus   = 2.45e-6
    M_earth   = 3.00e-6
    M_mars    = 3.23e-7
    M_jupiter = 9.55e-4
    M_saturn  = 2.86e-4
    M_uranus  = 4.37e-5
    M_neptune = 5.15e-5
    masses = [M_sun,
              M_mercury,
              M_venus,
              M_earth,
              M_mars,
              M_jupiter,
              M_saturn,
              M_uranus,
              M_neptune]

    # Semi-major axes (in AU)
    a_mercury = 0.39
    a_venus   = 0.723
    a_earth   = 1.0
    a_mars    = 1.524
    a_jupiter = 5.204
    a_saturn  = 9.58
    a_uranus  = 19.2
    a_neptune = 30.1
    positions = [[0.0, 0.0, 0.0],
                 [a_mercury, 0.0, 0.0],
                 [a_venus,   0.0, 0.0],
                 [a_earth,   0.0, 0.0],
                 [a_mars,    0.0, 0.0],
                 [a_jupiter, 0.0, 0.0],
                 [a_saturn,  0.0, 0.0],
                 [a_uranus,  0.0, 0.0],
                 [a_neptune, 0.0, 0.0]]

    # Velocities for circular orbits (in AU/year)
    v_mercury = 2*math.pi/math.sqrt(a_mercury)
    v_venus   = 2*math.pi/math.sqrt(a_venus)
    v_earth   = 2*math.pi/math.sqrt(a_earth)
    v_mars    = 2*math.pi/math.sqrt(a_mars)
    v_jupiter = 2*math.pi/math.sqrt(a_jupiter)
    v_saturn  = 2*math.pi/math.sqrt(a_saturn)
    v_uranus  = 2*math.pi/math.sqrt(a_uranus)
    v_neptune = 2*math.pi/math.sqrt(a_neptune)
    velocities = [[0.0, 0.0, 0.0],
                  [0.0,  v_mercury, 0.0],
                  [0.0,  v_venus, 0.0],
                  [0.0,  v_earth, 0.0],
                  [0.0,  v_mars, 0.0],
                  [0.0,  v_jupiter, 0.0],
                  [0.0,  v_saturn, 0.0],
                  [0.0,  v_uranus, 0.0],
                  [0.0,  v_neptune, 0.0]]

    return {"t_ini":      t_ini,
            "t_end":      t_end,
            "N_steps":    N_steps,
            "masses":     masses,
            "positions":  positions,
            "velocities": velocities}

# ----- Sélecteur de preset -----

AVAILABLE_PRESETS = {"earth_sun": earth_sun,
                     "solar_system": solar_system}


def load_preset(name="default"):
    if name not in AVAILABLE_PRESETS: raise ValueError(f"Preset '{name}' unknown. Available presets: {list(AVAILABLE_PRESETS)}")
    return AVAILABLE_PRESETS[name]()
