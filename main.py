import math
from bodies import Body, System
from integrator import euler, rk4
from rhs import compute_dudt
from init import load_preset

# Constants
G = 4*math.pi**2

# Input parameters
config = load_preset("earth_sun")

# Récupération
t_ini   = config["t_ini"]
t_end   = config["t_end"]
N_steps = config["N_steps"]
masses     = config["masses"]     # [m1, ..., mN]
positions  = config["positions"]  # [[x1, y1], ..., [xN, yN]]
velocities = config["velocities"] # [[vx1, vy1], ..., [vxN, vyN]]

# Create the initial system state
N_bodies = len(masses)
bodies = [Body(masses[i], positions[i], velocities[i]) for i in range(N_bodies)]
system = System(bodies)

# Calcul des paramètres temporels
t = t_ini
dt = (t_end - t_ini)/N_steps

# Création du vecteur d'état u = [x1, y1, vx1, vy1, ..., xN, yN, vxN, vyN]
u = [component for body in bodies for component in (body.position + body.velocity)]

# Création du vecteur des masses m = [m1, ..., mN]
m = [body.mass for body in bodies]

# Initialisation des listes contenant les trajectoires des corps
traj_x = [[u[4*i]]     for i in range(N_bodies)]
traj_y = [[u[4*i + 1]] for i in range(N_bodies)]

for step in range(N_steps):

    # Intégration en t+dt
    u = rk4(t, u, dt, compute_dudt, m, G)

    # Extraction des positions [[x1, y1], ..., [xN, yN]] et vitesses [[vx1, vy1], ..., [vxN, vyN]] à partir de u
    positions  = [u[4*i : 4*i+2] for i in range(N_bodies)]
    velocities = [u[4*i+2 : 4*i+4] for i in range(N_bodies)]

    # Mise à jour de chaque corps contenu dans le système
    for i, body in enumerate(system.bodies):
        body.position = positions[i]
        body.velocity = velocities[i]

    # Incrémentation du temps
    t += dt

    for i, (x, y) in enumerate(positions):
        traj_x[i].append(x)
        traj_y[i].append(y)






from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.set_aspect("equal", "box")

xmin, xmax = -10, 10
ymin, ymax = -10, 10
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)

# Un point (Line2D) par corps
points = [ax.plot([], [], "o")[0] for _ in range(N_bodies)]

# ---- TEXTE POUR LE TEMPS ----
time_text = ax.text(0.02, 0.95, "", transform=ax.transAxes)

def init():
    for p in points:
        p.set_data([], [])
    time_text.set_text("")  # temps initial
    return points + [time_text]

def update(frame):
    for i, p in enumerate(points):
        p.set_data([traj_x[i][frame]], [traj_y[i][frame]])

    # Mise à jour du texte du temps
    time_text.set_text(f"t = {frame * dt:.2f}")

    return points + [time_text]

ani = FuncAnimation(
    fig,
    update,
    frames=len(traj_x[0]),
    init_func=init,
    interval=20,
    blit=True
)

plt.show()
