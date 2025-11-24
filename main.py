from bodies import Body, System
from accelerations import compute_accelerations

def compute_dfdt(t, f, m, G):
    # Nombre de corps
    N_bodies = len(m)

    # Extraction des positions [[x1, y1], ..., [xN, yN]] et vitesses [[vx1, vy1], ..., [vxN, vyN]] à partir de f
    positions  = [f[4*i : 4*i+2] for i in range(N_bodies)]
    velocities = [f[4*i+2 : 4*i+4] for i in range(N_bodies)]

    # Calcul des accélérations [[ax1, ay1], ..., [axN, ayN]]
    accelerations = compute_accelerations(positions, m, G)

    # Construction de l'état à intégrer [vx1, vy1, ax1, ay1, ..., vxN, vyN, axN, ayN]
    dfdt = [component for body in range(N_bodies) for component in (velocities[body] + accelerations[body])]
    return dfdt


def euler(f, dfdt, dt):
    f_new = [fi + dfi*dt for fi, dfi in zip(f, dfdt)]
    return f_new




G = 1.0

# Input parameters
N_bodies = 2
t_ini, t_end, N_steps = [0.0, 10.0, 1000]
m1, x1, y1, vx1, vy1 = [10.0, 0.0, 0.0, 0.0, 1.0]
m2, x2, y2, vx2, vy2 = [1.0, 1.0, 0.0, 0.0, -1.0]

# Create the initial system state
body1  = Body(m1, [x1, y1], [vx1, vy1])
body2  = Body(m2, [x2, y2], [vx2, vy2])
system = System([body1, body2])

# Récupération de tous les corps bodies = [body1, ..., body_N]
bodies = system.bodies

# Calcul des paramètres temporels
t = t_ini
dt = (t_end - t_ini)/N_steps

# Création du vecteur d'état f = [x1, y1, vx1, vy1, ..., xN, yN, vxN, vyN]
f = [component for body in bodies for component in (body.position + body.velocity)]

# Création du vecteur des masses m = [m1, ..., mN]
m = [body.mass for body in bodies]

# Initialisation des listes contenant les trajectoires des corps
traj_x = [[f[4*i]]     for i in range(N_bodies)]
traj_y = [[f[4*i + 1]] for i in range(N_bodies)]

for step in range(N_steps):
    # Calcul des dérivées (rhs)
    dfdt = compute_dfdt(t, f, m, G)

    # Intégration en t+dt
    f = euler(f, dfdt, dt)

    # Extraction des positions [[x1, y1], ..., [xN, yN]] et vitesses [[vx1, vy1], ..., [vxN, vyN]] à partir de f
    positions  = [f[4*i : 4*i+2] for i in range(N_bodies)]
    velocities = [f[4*i+2 : 4*i+4] for i in range(N_bodies)]

    # Mise à jour de chaque corps contenu dans le système
    for i, body in enumerate(system.bodies):
        body.position = positions[i]
        body.velocity = velocities[i]

    # Incrémentation du temps
    t += dt

    for i, (x, y) in enumerate(positions):
        traj_x[i].append(x)
        traj_y[i].append(y)






# ----- Animation avec Matplotlib -----
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.set_aspect("equal", "box")

# Déterminer les limites du graphe
all_x = [x for xs in traj_x for x in xs]
all_y = [y for ys in traj_y for y in ys]
margin = 0.2
xmin, xmax = -10, 10
ymin, ymax = -10, 10
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)

# Un point (Line2D) par corps
points = [ax.plot([], [], "o")[0] for _ in range(N_bodies)]

def init():
    for p in points:
        p.set_data([], [])
    return points

def update(frame):
    for i, p in enumerate(points):
        # IMPORTANT : mettre des listes, pas des scalaires
        p.set_data([traj_x[i][frame]], [traj_y[i][frame]])
    return points

ani = FuncAnimation(
    fig,
    update,
    frames=len(traj_x[0]),
    init_func=init,
    interval=20,
    blit=True
)

plt.show()







## Input parameters
#t_end = 10
#N_steps = 100
#m1, x1, y1, vx1, vy1 = [1.0, 0.0, 0.0, 0.0, 1.0]
#m2, x2, y2, vx2, vy2 = [1.0, 1.0, 0.0, 0.0, -1.0]
#
## Initial states
#Y0 = [x1, y1, vx1, vy1, x2, y2, vx2, vy2]
#M0 = [m1, m2]
#
## Temps d'intégration
#T = np.linspace(0, t_end, N_steps)
#
#def rhs(Y, t, M, G):
#    """
#    Right-hand side of the ODE system for 2 bodies:
#    Y = [x1, y1, vx1, vy1, x2, y2, vx2, vy2]
#    dY/dt = [vx1, vy1, ax1, ay1, vx2, vy2, ax2, ay2]
#    """
#
#    # Unpack state vector and create bodies
#    x1, y1, vx1, vy1, x2, y2, vx2, vy2 = Y
#    m1, m2 = M
#
#    # Create the current system state
#    b1 = Body(m1, [x1, y1], [vx1, vy1])
#    b2 = Body(m2, [x2, y2], [vx2, vy2])
#
#    # Create the current system state
#    system = System([b1, b2])
#
#    # Compute accelerations with current system state
#    accelerations = compute_accelerations(system, G)
#    ax1, ay1 = accelerations[0]
#    ax2, ay2 = accelerations[1]
#
#    # Build dY/dt
#    dydt1 = vx1 # dx1/dt
#    dydt2 = vy1 # dy1/dt
#    dydt3 = ax1 # dvx1/dt
#    dydt4 = ay1 # dvy1/dt
#    dydt5 = vx2 # dx2/dt
#    dydt6 = vy2 # dy2/dt
#    dydt7 = ax2 # dvx2/dt
#    dydt8 = ay2 # dvy2/dt
#    dYdt = [dydt1, dydt2, dydt3, dydt4, dydt5, dydt6, dydt7, dydt8]
#    return dYdt
#
#solution = odeint(rhs, Y0, T, args=(M0, G))
