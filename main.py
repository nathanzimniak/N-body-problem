import math
from bodies import Body, System
from integrator import euler, rk4
from rhs import compute_dudt
from init import load_preset

# Constants
G = 4*math.pi**2

# Input parameters
config = load_preset("inner_solar_system")  # Choix du preset ("earth_sun" ou "solar_system")

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
traj_y = [[u[6*i+1]] for i in range(N_bodies)]
traj_z = [[u[6*i+2]] for i in range(N_bodies)]

# Time integration loop
for step in range(N_steps):
    # Integration at t+dt
    u = rk4(t, u, dt, compute_dudt, m, G)

    # Extraction of positions [[x1, y1, z1], ..., [xN, yN, zN]] and velocities [[vx1, vy1, vz1], ..., [vxN, vyN, vzN]] from u
    positions  = [u[6*i:6*i+3] for i in range(N_bodies)]
    velocities = [u[6*i+3:6*i+6] for i in range(N_bodies)]

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










# User parameters for visualization
visual_params = {"trail_length": 50,
                 "point_colors":      ["#FFB81F", "#6E6D88", "#C39531", "#006FFF", "#FF2F00"],
                 "point_edge_colors": ["#FFB81F", "#6E6D88", "#C39531", "#006FFF", "#FF2F00"],
                 "trail_colors":      ["#FFB81F", "#6E6D88", "#C39531", "#006FFF", "#FF2F00"],
                 "point_sizes":       [13, 3, 5, 6, 4],
                 "point_edge_widths": [15/5, 3/5, 5/5, 6/5, 4/5],
                 "trail_widths":      [15/3, 3/3, 5/3, 6/3, 4/3],
                 "axis_limits":       [-2.0, 2.0, -2.0, 2.0, -2.0, 2.0],
                 "elevation_angle": 35,
                 "azimuthal_angle": 45}

from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

# Visualization setup
point_sizes       = visual_params["point_sizes"]
point_edge_widths = visual_params["point_edge_widths"]
trail_widths      = visual_params["trail_widths"]
point_colors      = visual_params["point_colors"]
point_edge_colors = visual_params["point_edge_colors"]
trail_colors      = visual_params["trail_colors"]
trail_length      = visual_params["trail_length"]
axis_limits       = visual_params["axis_limits"]
elevation_angle   = visual_params["elevation_angle"]
azimuthal_angle   = visual_params["azimuthal_angle"]

# Dark mode
plt.style.use('dark_background')

# Figure and 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# Remove background panes
ax.xaxis.set_pane_color((0,0,0,0))
ax.yaxis.set_pane_color((0,0,0,0))
ax.zaxis.set_pane_color((0,0,0,0))

# Grid style
ax.xaxis._axinfo["grid"]["color"] = (1,1,1,0.1)
ax.yaxis._axinfo["grid"]["color"] = (1,1,1,0.1)
ax.zaxis._axinfo["grid"]["color"] = (1,1,1,0.1)

ax.zaxis.set_rotate_label(False)

# Axis limits
ax.set_xlim(axis_limits[0], axis_limits[1])
ax.set_ylim(axis_limits[2], axis_limits[3])
ax.set_zlim(axis_limits[4], axis_limits[5])

# Axis labels
ax.set_xlabel("x (UA)")
ax.set_ylabel("y (UA)")
ax.set_zlabel("z (UA)", rotation=90)

# View angle
ax.view_init(elevation_angle, azimuthal_angle)

# Points
points = [ax.plot([], [], [], "o", markersize=point_sizes[i], markerfacecolor=point_colors[i], markeredgecolor=point_edge_colors[i], markeredgewidth=point_edge_widths[i])[0] for i in range(N_bodies)]

# Trails
trails = [ax.plot([], [], [], "-", color=trail_colors[i], linewidth=trail_widths[i])[0] for i in range(N_bodies)]

# Time text
time_text = ax.text2D(0.02, 0.95, "", transform=ax.transAxes)

# Animation initialization function
def init():
    for p in points:
        p.set_data([], [])
        p.set_3d_properties([])
    for tr in trails:
        tr.set_data([], [])
        tr.set_3d_properties([])
    time_text.set_text("")
    return trails + points + [time_text]

# Animation update function
def update(frame):
    for i, (p, tr) in enumerate(zip(points, trails)):
        x = traj_x[i][frame]
        y = traj_y[i][frame]
        z = traj_z[i][frame]

        p.set_data([x], [y])
        p.set_3d_properties([z])

        start = 0 if trail_length is None else max(0, frame + 1 - trail_length)

        xs = traj_x[i][start:frame+1]
        ys = traj_y[i][start:frame+1]
        zs = traj_z[i][start:frame+1]

        tr.set_data(xs, ys)
        tr.set_3d_properties(zs)

    time_text.set_text(f"t = {frame * dt:.2f}")
    return trails + points + [time_text]

# Create animation
ani = FuncAnimation(fig, update, frames=len(traj_x[0]), init_func=init, interval=20, blit=True)

plt.show()