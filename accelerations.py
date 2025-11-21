from bodies import System
import math

def compute_accelerations(system, G):
    """
    Compute the gravitational accelerations acting on each body
    in an N-body system, using Newton's law.
    """
    # Extract masses and positions from the system
    bodies    = system.bodies          # [body1, body2, ...]
    masses    = system.get_masses()    # [m1, m2, ...]
    positions = system.get_positions() # [[x1, y1], [x2, y2], ...]

    # Number of bodies in the system
    N_bodies = len(bodies)

    # Initialize the acceleration vectors for all bodies
    accelerations = [[0.0, 0.0] for _ in range(N_bodies)] # [[ax1, ay1], [ax2, ay2], ...]

    # Loop over each body
    for body in range(N_bodies):
        # Mass and position of the current body
        mass_body      = masses[body]
        x_body, y_body = positions[body]

        # Compute interactions with every other body
        for other_body in range(N_bodies):
            # Skip self-interaction
            if body == other_body: continue

            # Mass and position of the other body
            mass_other_body = masses[other_body]
            x_other_body, y_other_body = positions[other_body]

            # Distance between both bodies
            d = math.sqrt((x_other_body - x_body)**2 + (y_other_body - y_body)**2)
            if d == 0: raise RuntimeError(f"Collision detected between bodies {body} and {other_body}")

            # Compute gravitational force exerted on 'body' by 'other_body'
            fx = (G*mass_body*mass_other_body/d**3)*(x_other_body - x_body)
            fy = (G*mass_body*mass_other_body/d**3)*(y_other_body - y_body)

            # Compute acceleration of 'body' induced by 'other_body'
            ax = fx/mass_body
            ay = fy/mass_body

            # Add contribution from this interaction
            accelerations[body][0] += ax
            accelerations[body][1] += ay
    return accelerations