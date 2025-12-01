import math
from bodies import Body, System
from integrator import euler, rk4
from rhs import compute_dudt
from init import load_preset
from plot import plot_trajectories

# Constants
G = 4*math.pi**2

# Input parameters
config = load_preset("three_body_3d_orbits")  # Choix du preset ("earth_sun" ou "solar_system")

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

# Visualization parameters
trail_length      = config["trail_length"]
point_colors      = config["point_colors"]
point_edge_colors = config["point_edge_colors"]
trail_colors      = config["trail_colors"]
point_sizes       = config["point_sizes"]
point_edge_widths = config["point_edge_widths"]
trail_widths      = config["trail_widths"]
axis_limits       = config["axis_limits"]
elevation_angle   = config["elevation_angle"]
azimuthal_angle   = config["azimuthal_angle"]

# Pack visual parameters into a dictionary
visual_params = {"trail_length":      trail_length,
                 "point_colors":      point_colors,
                 "point_edge_colors": point_edge_colors,
                 "trail_colors":      trail_colors,
                 "point_sizes":       point_sizes,
                 "point_edge_widths": point_edge_widths,
                 "trail_widths":      trail_widths,
                 "axis_limits":       axis_limits,
                 "elevation_angle":   elevation_angle,
                 "azimuthal_angle":   azimuthal_angle}

# Plot the trajectories
plot_trajectories(traj_x, traj_y, traj_z, dt, N_bodies, visual_params)