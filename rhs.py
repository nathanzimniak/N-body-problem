from accelerations import compute_accelerations

def compute_dudt(t, u, m, G):
    # Nombre de corps
    N_bodies = len(m)

    # Extraction des positions [[x1, y1], ..., [xN, yN]] et vitesses [[vx1, vy1], ..., [vxN, vyN]] à partir de u
    positions  = [u[4*i : 4*i+2] for i in range(N_bodies)]
    velocities = [u[4*i+2 : 4*i+4] for i in range(N_bodies)]

    # Calcul des accélérations [[ax1, ay1], ..., [axN, ayN]]
    accelerations = compute_accelerations(positions, m, G)

    # Construction de l'état à intégrer [vx1, vy1, ax1, ay1, ..., vxN, vyN, axN, ayN]
    dudt = [component for body in range(N_bodies) for component in (velocities[body] + accelerations[body])]
    return dudt