#include "solver.hpp"
#include "setups.hpp"
#include "time_integrators.hpp"


Simulation setup_eight(
) {
    // Number of bodies.
    const std::size_t n_bodies = 3;

    // Physical parameters.
    const double G   = 1.0;                  // Gravitational constant.
    const double eps = 1e-3;                 // Very small softening to preserve the figure-eight orbit.
    std::vector<double> mass(n_bodies, 1.0); // Equal masses.

    Params params {
        .G    = G,
        .eps  = eps,
        .mass = mass
    };

    // Time parameters.
    const double t_start = 0.0;  // Initial time.
    const double t_end   = 20.0; // Final time.
    const double dt      = 1e-4; // Small time step for good orbit preservation.

    TimeConfig time {
        .t_start = t_start,
        .t_end   = t_end,
        .dt      = dt
    };

    // Initial conditions.
    State bodies {
        .x  = std::vector<double>(n_bodies),
        .y  = std::vector<double>(n_bodies),
        .z  = std::vector<double>(n_bodies),
        .vx = std::vector<double>(n_bodies),
        .vy = std::vector<double>(n_bodies),
        .vz = std::vector<double>(n_bodies)
    };

    // Standard figure-eight initial conditions (equal-mass three-body choreography).
    bodies.x[0]  =  0.97000436;
    bodies.y[0]  = -0.24308753;
    bodies.z[0]  =  0.0;
    bodies.vx[0] =  0.4662036850;
    bodies.vy[0] =  0.4323657300;
    bodies.vz[0] =  0.0;

    bodies.x[1]  = -0.97000436;
    bodies.y[1]  =  0.24308753;
    bodies.z[1]  =  0.0;
    bodies.vx[1] =  0.4662036850;
    bodies.vy[1] =  0.4323657300;
    bodies.vz[1] =  0.0;

    bodies.x[2]  =  0.0;
    bodies.y[2]  =  0.0;
    bodies.z[2]  =  0.0;
    bodies.vx[2] = -0.93240737;
    bodies.vy[2] = -0.86473146;
    bodies.vz[2] =  0.0;

    // Time integrator.
    Integrator integrator = rk4;

    // Save configuration.
    const std::string directory = "./outputs/eight"; // Output directory for the HDF5 files.
    const int output_frequency = 50;                 // Save frequency.

    SaveConfig save {
        .directory = directory,
        .frequency = output_frequency
    };

    return Simulation {
        .bodies      = bodies,
        .params      = params,
        .time        = time,
        .integrator  = integrator,
        .save        = save,
    };
}


// Register the setup in the global registry at program startup.
SetupRegistrar register_eight("eight", setup_eight);