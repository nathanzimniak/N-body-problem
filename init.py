

def two_body_default():
    return {"t_ini": 0.0,
            "t_end": 10.0,
            "N_steps": 5000,
            "masses": [1.0, 1.0],
            "positions": [[0.0, 0.0], [1.0, 1.0]],
            "velocities": [[1.0, 10.0], [-1.0, 1.0]]
    }


def earth_sun():
    # Un exemple réaliste (unités astronomiques)
    return {"t_ini": 0.0,
            "t_end": 1.0,
            "N_steps": 356,
            "masses": [1.0, 3e-6],
            "positions": [[0.0, 0.0], [1.0, 0.0]],
            "velocities": [[0.0, 0.0], [0.0, 2*3.141592]]}


def chaotic_three_body():
    return {"t_ini": 0.0,
            "t_end": 20.0,
            "N_steps": 20000,
            "masses": [1.0, 1.0, 1.0],
            "positions": [[-1, 0], [1, 0], [0, 0.1]],
            "velocities": [[0.5, 0.3], [-0.5, 0.3], [0.0, -0.6]]}


# ----- Sélecteur de preset -----

AVAILABLE_PRESETS = {
    "default": two_body_default,
    "earth_sun": earth_sun,
    "three_body": chaotic_three_body,
}


def load_preset(name="default"):
    """
    Retourne un dictionnaire contenant les conditions initiales.
    """
    if name not in AVAILABLE_PRESETS:
        raise ValueError(f"Preset '{name}' inconnu. Disponibles : {list(AVAILABLE_PRESETS)}")

    return AVAILABLE_PRESETS[name]()
