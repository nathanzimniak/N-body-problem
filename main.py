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





from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
plt.style.use('dark_background')

# ---------------------------
#   PARAMÈTRES GRAPHIQUES
# ---------------------------

visual_params = {
    "trail_length": 50, # nombre de points dans la traînée (None = complet)
    "point_colors":      ["#FFB81F", "#6E6D88", "#C39531", "#006FFF", "#FF2F00"], # liste de couleurs ou None
    "point_edge_colors": ["#FFB81F", "#6E6D88", "#C39531", "#006FFF", "#FF2F00"], # liste de couleurs de bord par corps
    "trail_colors":      ["#FFB81F", "#6E6D88", "#C39531", "#006FFF", "#FF2F00"], # liste de couleurs ou None
    "point_sizes":       [13, 3, 5, 6, 4],           # liste de tailles des points ou None
    "point_edge_widths": [15/5, 3/5, 5/5, 6/5, 4/5], # liste d'épaisseurs de bord par corps
    "trail_widths":      [15/3, 3/3, 5/3, 6/3, 4/3], # liste de largeurs des traits ou None
}

# Palette par défaut
default_colors = plt.cm.tab10(range(N_bodies))

# Couleurs des points et des traînées
point_colors = visual_params["point_colors"] or default_colors
trail_colors = visual_params["trail_colors"] or default_colors

# Tailles des points
point_sizes = (
    [6] * N_bodies 
    if visual_params["point_sizes"] is None 
    else visual_params["point_sizes"]
)

# Largeurs des traînées
trail_widths = (
    [1.0] * N_bodies 
    if visual_params["trail_widths"] is None 
    else visual_params["trail_widths"]
)

# —— NOUVEAU : Couleur des contours ——
point_edge_colors = (
    ["black"] * N_bodies
    if visual_params["point_edge_colors"] is None
    else visual_params["point_edge_colors"]
)

# —— NOUVEAU : Épaisseur des contours ——
point_edge_widths = (
    [0.8] * N_bodies
    if visual_params["point_edge_widths"] is None
    else visual_params["point_edge_widths"]
)

TRAIL_LENGTH = visual_params["trail_length"]

# ---------------------------
#      ANIMATION
# ---------------------------

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
# Panneaux transparents
ax.xaxis.set_pane_color((0,0,0,0))
ax.yaxis.set_pane_color((0,0,0,0))
ax.zaxis.set_pane_color((0,0,0,0))
# Grille invisible
ax.xaxis._axinfo["grid"]["color"] = (1,1,1,0.1)
ax.yaxis._axinfo["grid"]["color"] = (1,1,1,0.1)
ax.zaxis._axinfo["grid"]["color"] = (1,1,1,0.1)

# Limites 3D
all_x = [x for xs in traj_x for x in xs]
all_y = [y for ys in traj_y for y in ys]
all_z = [z for zs in traj_z for z in zs]

R = max(max(map(abs, all_x + all_y + all_z)), 1.0)
R = min(R, 30.0)

ax.set_xlim(-R, R)
ax.set_ylim(-R, R)
ax.set_zlim(-R, R)

ax.set_xlabel("x (UA)")
ax.set_ylabel("y (UA)")
ax.set_zlabel("z (UA)")

elevation_angle = 35
azimuthal_angle = 45
ax.view_init(elevation_angle, azimuthal_angle)

# Points des corps (3D)
points = [
    ax.plot(
        [], [], [],
        "o",
        markersize=point_sizes[i],
        markerfacecolor=point_colors[i],
        markeredgecolor=point_edge_colors[i],     # <<< nouveau
        markeredgewidth=point_edge_widths[i]      # <<< nouveau
    )[0]
    for i in range(N_bodies)
]

# Traînées
trails = [
    ax.plot(
        [], [], [],
        "-",
        color=trail_colors[i],
        linewidth=trail_widths[i]
    )[0]
    for i in range(N_bodies)
]

# Texte du temps
time_text = ax.text2D(0.02, 0.95, "", transform=ax.transAxes)


def init():
    for p in points:
        p.set_data([], [])
        p.set_3d_properties([])
    for tr in trails:
        tr.set_data([], [])
        tr.set_3d_properties([])
    time_text.set_text("")
    return trails + points + [time_text]

def update(frame):
    for i, (p, tr) in enumerate(zip(points, trails)):
        x = traj_x[i][frame]
        y = traj_y[i][frame]
        z = traj_z[i][frame]

        p.set_data([x], [y])
        p.set_3d_properties([z])

        start = 0 if TRAIL_LENGTH is None else max(0, frame + 1 - TRAIL_LENGTH)

        xs = traj_x[i][start:frame+1]
        ys = traj_y[i][start:frame+1]
        zs = traj_z[i][start:frame+1]

        tr.set_data(xs, ys)
        tr.set_3d_properties(zs)

    time_text.set_text(f"t = {frame * dt:.2f}")
    return trails + points + [time_text]


ani = FuncAnimation(
    fig,
    update,
    frames=len(traj_x[0]),
    init_func=init,
    interval=20,
    blit=True
)

plt.show()
