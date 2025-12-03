from accelerations import compute_accelerations

def compute_dudt(t, u, m, G):
    # Nombre de corps
    N_bodies = len(m)

    # Extraction des positions [[x1, y1, z1], ..., [xN, yN, zN]] et vitesses [[vx1, vy1, vz1], ..., [vxN, vyN, vzN]] à partir de u
    positions  = [u[6*i     : 6*i+3] for i in range(N_bodies)]
    velocities = [u[6*i + 3 : 6*i+6] for i in range(N_bodies)]

    # Calcul des accélérations [[ax1, ay1], ..., [axN, ayN]]
    accelerations = compute_accelerations(positions, m, G)

    # Construction de l'état à intégrer [vx1, vy1, ax1, ay1, ..., vxN, vyN, axN, ayN]
    dudt = [component for body in range(N_bodies) for component in (velocities[body] + accelerations[body])]
    return dudt