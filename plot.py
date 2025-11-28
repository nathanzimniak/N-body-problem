from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

def plot_trajectories(traj_x, traj_y, traj_z, dt, N_bodies, visual_params):
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
    xmin, xmax, ymin, ymax, zmin, zmax = axis_limits
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_zlim(zmin, zmax)

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
    time_text = ax.text2D(0.5, 1.0, "", ha="center", va="bottom", fontsize=11, transform=ax.transAxes)

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

        time_text.set_text(f"t = {frame:.0f} days")
        return trails + points + [time_text]

    # Create animation
    ani = FuncAnimation(fig, update, frames=len(traj_x[0]), init_func=init, interval=40, blit=False)

    plt.show()