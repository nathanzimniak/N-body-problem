import math
from bodies import Body, System
from integrator import euler, rk4
from rhs import compute_dudt
from init import load_preset

# Constants
G = 4*math.pi**2

# Input parameters
config = load_preset("earth_sun")  # Choix du preset ("earth_sun" ou "solar_system")

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

# Create the state vector u = [x1, y1, z1, vx1, vy1, vz1, ..., xN, yN, zN, vxN, vyN, vzN]
u = [component for body in bodies for component in (body.position + body.velocity)]

# Create the mass vector m = [m1, ..., mN]
m = [body.mass for body in bodies]

# Initialization of lists containing the trajectories of the bodies
traj_x = [[u[6*i]]     for i in range(N_bodies)]
traj_y = [[u[6*i + 1]] for i in range(N_bodies)]
traj_z = [[u[6*i + 2]] for i in range(N_bodies)]

# Time integration loop
for step in range(N_steps):
    # Integration at t+dt
    u = rk4(t, u, dt, compute_dudt, m, G)

    # Extraction of positions [[x1, y1, z1], ..., [xN, yN, zN]] and velocities [[vx1, vy1, vz1], ..., [vxN, vyN, vzN]] from u
    positions  = [u[6*i     : 6*i+3] for i in range(N_bodies)]
    velocities = [u[6*i + 3 : 6*i+6] for i in range(N_bodies)]

    # Update each body contained in the system
    for i, body in enumerate(system.bodies):
        body.position = positions[i]
        body.velocity = velocities[i]

    # Store positions
    for i, (x, y, z) in enumerate(positions):
        traj_x[i].append(x)
        traj_y[i].append(y)
        traj_z[i].append(z)

    # Time increment
    t += dt






from mpl_toolkits.mplot3d import Axes3D  # juste pour activer 3D
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# Limites 3D
all_x = [x for xs in traj_x for x in xs]
all_y = [y for ys in traj_y for y in ys]
all_z = [z for zs in traj_z for z in zs]

R = max(max(map(abs, all_x + all_y + all_z)), 1.0)
R = min(R, 30.0)  # limite max si tu veux

ax.set_xlim(-R, R)
ax.set_ylim(-R, R)
ax.set_zlim(-R, R)

# Un point par corps
points = [ax.plot([], [], [], "o")[0] for _ in range(N_bodies)]

time_text = ax.text2D(0.02, 0.95, "", transform=ax.transAxes)

def init():
    for p in points:
        p.set_data([], [])
        p.set_3d_properties([])
    time_text.set_text("")
    return points + [time_text]

def update(frame):
    for i, p in enumerate(points):
        x = traj_x[i][frame]
        y = traj_y[i][frame]
        z = traj_z[i][frame]
        p.set_data([x], [y])
        p.set_3d_properties([z])

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
