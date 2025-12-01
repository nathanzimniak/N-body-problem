from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

#def plot_trajectories(traj_x, traj_y, traj_z, dt, N_bodies, visual_params):
#    # Visualization setup
#    point_sizes       = visual_params["point_sizes"]
#    point_edge_widths = visual_params["point_edge_widths"]
#    trail_widths      = visual_params["trail_widths"]
#    point_colors      = visual_params["point_colors"]
#    point_edge_colors = visual_params["point_edge_colors"]
#    trail_colors      = visual_params["trail_colors"]
#    trail_length      = visual_params["trail_length"]
#    axis_limits       = visual_params["axis_limits"]
#    elevation_angle   = visual_params["elevation_angle"]
#    azimuthal_angle   = visual_params["azimuthal_angle"]
#
#    # Dark mode
#    plt.style.use('dark_background')
#
#    # Figure and 3D axis
#    fig = plt.figure()
#    ax = fig.add_subplot(111, projection="3d")
#
#    # Remove background panes
#    ax.xaxis.set_pane_color((0,0,0,0))
#    ax.yaxis.set_pane_color((0,0,0,0))
#    ax.zaxis.set_pane_color((0,0,0,0))
#
#    # Grid style
#    ax.xaxis._axinfo["grid"]["color"] = (1,1,1,0.1)
#    ax.yaxis._axinfo["grid"]["color"] = (1,1,1,0.1)
#    ax.zaxis._axinfo["grid"]["color"] = (1,1,1,0.1)
#
#    ax.zaxis.set_rotate_label(False)
#
#    # Axis limits
#    xmin, xmax, ymin, ymax, zmin, zmax = axis_limits
#    ax.set_xlim(xmin, xmax)
#    ax.set_ylim(ymin, ymax)
#    ax.set_zlim(zmin, zmax)
#
#    # Axis labels
#    ax.set_xlabel("x (UA)")
#    ax.set_ylabel("y (UA)")
#    ax.set_zlabel("z (UA)", rotation=90)
#
#    # View angle
#    ax.view_init(elevation_angle, azimuthal_angle)
#
#    # Points
#    points = [ax.plot([], [], [], "o", markersize=point_sizes[i], markerfacecolor=point_colors[i], markeredgecolor=point_edge_colors[i], markeredgewidth=point_edge_widths[i])[0] for i in range(N_bodies)]
#
#    # Trails
#    trails = [ax.plot([], [], [], "-", color=trail_colors[i], linewidth=trail_widths[i])[0] for i in range(N_bodies)]
#
#    # Time text
#    time_text = ax.text2D(0.5, 1.0, "", ha="center", va="bottom", fontsize=11, transform=ax.transAxes)
#
#    # Animation initialization function
#    def init():
#        for p in points:
#            p.set_data([], [])
#            p.set_3d_properties([])
#        for tr in trails:
#            tr.set_data([], [])
#            tr.set_3d_properties([])
#        time_text.set_text("")
#        return trails + points + [time_text]
#
#    # Animation update function
#    def update(frame):
#        for i, (p, tr) in enumerate(zip(points, trails)):
#            x = traj_x[i][frame]
#            y = traj_y[i][frame]
#            z = traj_z[i][frame]
#
#            p.set_data([x], [y])
#            p.set_3d_properties([z])
#
#            start = 0 if trail_length is None else max(0, frame + 1 - trail_length)
#
#            xs = traj_x[i][start:frame+1]
#            ys = traj_y[i][start:frame+1]
#            zs = traj_z[i][start:frame+1]
#
#            tr.set_data(xs, ys)
#            tr.set_3d_properties(zs)
#
#        time_text.set_text(f"t = {frame:.0f} days")
#        return trails + points + [time_text]
#
#    # Create animation
#    ani = FuncAnimation(fig, update, frames=len(traj_x[0]), init_func=init, interval=40, blit=False)
#
#    plt.show()

import math
import numpy as np
import pyvista as pv


def plot_trajectories(traj_x, traj_y, traj_z, dt, N_bodies, visual_params):
    """
    Visualisation 3D animée avec PyVista (sans glow, trails propres).

    traj_x, traj_y, traj_z : listes/arrays de shape (N_bodies, n_frames)
    dt                     : pas de temps (en jours, pour l'affichage)
    N_bodies               : nombre de corps
    visual_params          : dict avec :
        - point_sizes
        - point_edge_widths (ignoré ici)
        - trail_widths
        - point_colors
        - point_edge_colors (ignoré ici)
        - trail_colors
        - trail_length
        - axis_limits = (xmin, xmax, ymin, ymax, zmin, zmax)
        - elevation_angle (deg)
        - azimuthal_angle (deg)
    """

    point_sizes       = visual_params["point_sizes"]
    trail_widths      = visual_params["trail_widths"]
    point_colors      = visual_params["point_colors"]
    trail_colors      = visual_params["trail_colors"]
    trail_length      = visual_params["trail_length"]
    axis_limits       = visual_params["axis_limits"]
    elevation_angle   = visual_params["elevation_angle"]
    azimuthal_angle   = visual_params["azimuthal_angle"]

    xmin, xmax, ymin, ymax, zmin, zmax = axis_limits

    # Données -> numpy : shape (N_bodies, n_frames)
    traj_x = np.asarray(traj_x)
    traj_y = np.asarray(traj_y)
    traj_z = np.asarray(traj_z)
    n_frames = traj_x.shape[1]

    # ---------- Plotter ----------
    plotter = pv.Plotter()
    plotter.set_background("black")

    #plotter.show_bounds(
    #    bounds=(xmin, xmax, ymin, ymax, zmin, zmax),
    #    xtitle="x (UA)",
    #    ytitle="y (UA)",
    #    ztitle="z (UA)"
    #)

    #plotter.show_bounds(False)

    # ---------- Caméra (style Matplotlib) ----------
    cx, cy, cz = (xmin + xmax) / 2, (ymin + ymax) / 2, (zmin + zmax) / 2
    scene_size = max(xmax - xmin, ymax - ymin, zmax - zmin)
    if scene_size == 0:
        scene_size = 1.0

    r = 1.8 * scene_size

    elev = math.radians(elevation_angle)
    azim = math.radians(azimuthal_angle)

    eye = (
        cx + r * math.cos(elev) * math.cos(azim),
        cy + r * math.cos(elev) * math.sin(azim),
        cz + r * math.sin(elev),
    )
    plotter.camera_position = [eye, (cx, cy, cz), (0, 0, 1)]

    # ---------- Acteurs ----------
    sphere_actors = []   # corps
    trail_pds     = []   # géométrie des traînées

    base_radius = 0.015 * scene_size
    mean_size   = float(np.mean(point_sizes)) if len(point_sizes) > 0 else 1.0

    for i in range(N_bodies):
        x0 = float(traj_x[i, 0])
        y0 = float(traj_y[i, 0])
        z0 = float(traj_z[i, 0])

        # Rayon du corps
        radius = base_radius * (point_sizes[i] / mean_size)

        # --- Sphère du corps ---
        core_sphere = pv.Sphere(radius=radius)
        core_actor = plotter.add_mesh(
            core_sphere,
            color=point_colors[i],
            smooth_shading=True,
        )
        core_actor.position = (x0, y0, z0)
        sphere_actors.append(core_actor)

        # --- Traînée ---
        pd_trail = pv.PolyData()
        pts0 = np.array([[x0, y0, z0]])
        pd_trail.points = pts0
        pd_trail.lines = np.array([1, 0], dtype=np.int64)
        trail_pds.append(pd_trail)

        # On rend la ligne comme un "tube" pour un aspect régulier
        plotter.add_mesh(
            pd_trail,
            color=trail_colors[i],
            line_width=trail_widths[i],
            lighting=False,             # évite les ombres bizarres
            render_lines_as_tubes=True  # tubes jolis et uniformes
        )

    # Texte du temps
    plotter.add_text(
        "t = 0 days",
        name="time_text",
        position="upper_edge",
        color="white",
        font_size=12,
    )

    # ---------- Callback du timer ----------
    def callback(step: int):
        f = step % n_frames
        t_days = f * dt

        for i in range(N_bodies):
            px = float(traj_x[i, f])
            py = float(traj_y[i, f])
            pz = float(traj_z[i, f])

            # Bouger le corps
            sphere_actors[i].position = (px, py, pz)

            # Mettre à jour la traînée
            start = 0 if trail_length is None else max(0, f + 1 - trail_length)

            xs = traj_x[i, start:f + 1]
            ys = traj_y[i, start:f + 1]
            zs = traj_z[i, start:f + 1]

            pts = np.column_stack((xs, ys, zs))
            trail_pds[i].points = pts

            npts = pts.shape[0]
            trail_pds[i].lines = np.hstack(
                ([npts], np.arange(npts, dtype=np.int64))
            )

        plotter.add_text(
            f"t = {t_days:.0f} days",
            name="time_text",
            position="upper_edge",
            color="white",
            font_size=12,
        )

    # ---------- Timer & lancement ----------
    plotter.add_timer_event(
        max_steps=10_000,   # on boucle via f % n_frames
        duration=40,        # ms → ~25 FPS
        callback=callback,
    )

    plotter.show()
