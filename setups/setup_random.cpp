#include "solver.hpp"
#include "setups.hpp"
#include "time_integrators.hpp"

#include <random>


static double random_double(
    double min,
    double max
) {
    // Create a random number generator
    static std::mt19937 gen(std::random_device{}());

    // Define a uniform distribution between min and max.
    std::uniform_real_distribution<> dist(min, max);

    return dist(gen);
}

Simulation setup_random(
) {
    // Number of bodies.
    const std::size_t n_bodies = 10000;

    // Physical parameters.
    const double G = 1.0;               // Gravitational constant.
    const double eps = 5e-2;            // Softening parameter.
    std::vector<double> mass(n_bodies); // Masses of the bodies.

    for (std::size_t i = 0; i < n_bodies; ++i) {
        mass[i] = random_double(0.1, 10.0);
    }

    Params params {
        .G    = G,
        .eps  = eps,
        .mass = mass
    };

    // Time parameters.
    const double t_start = 0.0;   // Initial time.
    const double t_end   = 0.5;   // Final time.
    const double dt      = 0.001; // Time step.

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

    for (std::size_t i = 0; i < n_bodies; ++i) {
        bodies.x[i]  = random_double(-2.0, 2.0);
        bodies.y[i]  = random_double(-2.0, 2.0);
        bodies.z[i]  = random_double(-2.0, 2.0);
        bodies.vx[i] = random_double(-2.0, 2.0);
        bodies.vy[i] = random_double(-2.0, 2.0);
        bodies.vz[i] = random_double(-2.0, 2.0);
    }

    // Time integrator.
    Integrator integrator = rk4;

    // Save configuration.
    const std::string directory = "./outputs/random"; // Output directory for the HDF5 files.
    const int output_frequency = 50;                  // Save frequency.

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
SetupRegistrar register_random("random", setup_random);