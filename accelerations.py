from bodies import System
import math

def compute_accelerations(system, G):

    bodies = system.bodies             # [body1, body2, ...]
    masses    = system.get_masses()    # [m1, m2, ...]
    positions = system.get_positions() # [[x1, y1], [x2, y2], ...]

    # Nombre de corps
    N_bodies = len(bodies)

    # Accélérations des corps
    accelerations = [[0.0, 0.0] for _ in range(N_bodies)] # [[ax1, ay1], [ax2, ay2], ...]

    # Pour chaque corps
    for body in range(N_bodies):
        #Calcul de la masse du corps
        mass_body = masses[body]

        # Calcul de la position du corps
        x_body, y_body = positions[body]

        # Pour tous les autres corps
        for other_body in range(N_bodies):
            # Si l'autre corps est le corps considéré, ne pas calculer
            if body == other_body: continue

            #Calcul de la masse de l'autre corps
            mass_other_body = masses[other_body]

            # Calcul de la position de l'autre corps
            x_other_body, y_other_body = positions[other_body]

            # Calcul de la distance entre le corps et l'autre corps
            d = math.sqrt((x_other_body - x_body)**2 + (y_other_body - y_body)**2)

            if d == 0: raise RuntimeError(f"Collision détectée entre les corps {body} et {other_body}")

            # Calcul de la force exercée par l'autre corps sur le corps
            fx = (G*mass_body*mass_other_body/d**3)*(x_other_body - x_body)
            fy = (G*mass_body*mass_other_body/d**3)*(y_other_body - y_body)

            # Calcul de l'accélération du corps induite par l'autre corps
            ax = fx/mass_body
            ay = fy/mass_body

            # Ajout de l'accélération à l'accélération totale
            accelerations[body][0] += ax
            accelerations[body][1] += ay

    return accelerations