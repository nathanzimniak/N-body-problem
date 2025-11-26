import math
from bodies import Body, System
from integrator import euler, rk4
from rhs import compute_dudt
from init import load_preset

# Constants
G = 4*math.pi**2

# Input parameters
config = load_preset("solar_system")

# Extract configuration
t_ini      = config["t_ini"]
t_end      = config["t_end"]
N_steps    = config["N_steps"]
masses     = config["masses"]     # [m1, ..., mN]
positions  = config["positions"]  # [[x1, y1], ..., [xN, yN]]
velocities = config["velocities"] # [[vx1, vy1], ..., [vxN, vyN]]

# Create the initial system state
N_bodies = len(masses)
bodies = [Body(masses[i], positions[i], velocities[i]) for i in range(N_bodies)]
system = System(bodies)

# Compute time parameters
t = t_ini
dt = (t_end - t_ini)/N_steps

# Create the state vector u = [x1, y1, vx1, vy1, ..., xN, yN, vxN, vyN]
u = [component for body in bodies for component in (body.position + body.velocity)]

# Create the mass vector m = [m1, ..., mN]
m = [body.mass for body in bodies]

# Initialization of lists containing the trajectories of the bodies
traj_x = [[u[4*i]]     for i in range(N_bodies)]
traj_y = [[u[4*i + 1]] for i in range(N_bodies)]

for step in range(N_steps):

    # Integration at t+dt
    u = rk4(t, u, dt, compute_dudt, m, G)

    # Extraction of positions [[x1, y1], ..., [xN, yN]] and velocities [[vx1, vy1], ..., [vxN, vyN]] from u
    positions  = [u[4*i : 4*i+2] for i in range(N_bodies)]
    velocities = [u[4*i+2 : 4*i+4] for i in range(N_bodies)]

    # Update each body contained in the system
    for i, body in enumerate(system.bodies):
        body.position = positions[i]
        body.velocity = velocities[i]

    # Time increment
    t += dt

    for i, (x, y) in enumerate(positions):
        traj_x[i].append(x)
        traj_y[i].append(y)






from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.set_aspect("equal", "box")

all_x = [x for xs in traj_x for x in xs]
all_y = [y for ys in traj_y for y in ys]

xmin, xmax = min(all_x), max(all_x)
ymin, ymax = min(all_y), max(all_y)

xmin = max(xmin, -30) - 1
xmax = min(xmax,  30) + 1
ymin = max(ymin, -30) - 1
ymax = min(ymax,  30) + 1

xmin = -max(abs(xmin), abs(xmax), abs(ymin), abs(ymax))
ymin = -max(abs(xmin), abs(xmax), abs(ymin), abs(ymax))
xmax = max(abs(xmin), abs(xmax), abs(ymin), abs(ymax))
ymax = max(abs(xmin), abs(xmax), abs(ymin), abs(ymax))

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
