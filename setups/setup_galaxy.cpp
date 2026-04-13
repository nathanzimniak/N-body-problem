#include "solver.hpp"
#include "setups.hpp"
#include "time_integrators.hpp"

#include <cmath>
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


Simulation setup_galaxy(
) {
    // Number of bodies.
    const std::size_t n_bodies = 50000;

    // Physical parameters.
    const double G = 1.0;                             // Gravitational constant.
    const double eps = 0.1;                           // Softening parameter.
    std::vector<double> mass(n_bodies, 1.0/n_bodies); // Masses of the bodies.

    Params params {
        .G    = G,
        .eps  = eps,
        .mass = mass
    };

    // Time parameters.
    const double t_start = 0.0;   // Initial time.
    const double t_end   = 3.0;   // Final time.
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

    const double R_d   = 2.0;   // Disk scale radius.
    const double z0    = 0.08;  // Disk thickness.
    const double r_max = 10.0;  // Radial cutoff.
    constexpr double pi = 3.14159265358979323846;

    // Total mass.
    double M_total = 0.0;
    for (std::size_t i = 0; i < n_bodies; ++i) {
        M_total += mass[i];
    }

    for (std::size_t i = 0; i < n_bodies; ++i) {

        // Exponential disk radius sampling with rejection.
        double r = 0.0;
        while (true) {
            double u = random_double(0.0, 1.0);
            r = -R_d * std::log(1.0 - u);
            if (r < r_max) break;
        }

        double phi = random_double(0.0, 2.0 * pi);

        // Perturbation m=2 to seed non-axisymmetric structure.
        double perturb = 1.0 + 0.05 * std::cos(2.0 * phi);
            
        // Thin disk geometry.
        bodies.x[i] = perturb * r * std::cos(phi);
        bodies.y[i] = perturb * r * std::sin(phi);
        bodies.z[i] = random_double(-z0, z0);

        // Simple enclosed mass model for disk-like rotation curve.
        double M_enc = M_total * (1.0 - std::exp(-r / R_d) * (1.0 + r / R_d));

        // Circular speed.
        double v_c = std::sqrt(G * M_enc / std::max(r, 1e-3));

        // Add a little velocity dispersion to seed spiral structure.
        double sigma_r   = 0.04 * v_c;
        double sigma_phi = 0.025 * v_c;
        double sigma_z   = 0.012 * v_c;

        // Basis vectors.
        double erx = std::cos(phi);
        double ery = std::sin(phi);
        double epx = -std::sin(phi);
        double epy =  std::cos(phi);

        // Small spiral seed in azimuthal velocity.
        double spiral_seed = 1.0 + 0.05 * std::cos(2.0 * phi);

        double v_r   = random_double(-sigma_r, sigma_r);
        double v_phi = v_c * spiral_seed + random_double(-sigma_phi, sigma_phi);
        double v_z   = random_double(-sigma_z, sigma_z);

        bodies.vx[i] = v_r * erx + v_phi * epx;
        bodies.vy[i] = v_r * ery + v_phi * epy;
        bodies.vz[i] = v_z;
    }

    double x_cm = 0.0, y_cm = 0.0, z_cm = 0.0;
    double vx_cm = 0.0, vy_cm = 0.0, vz_cm = 0.0;

    for (std::size_t i = 0; i < n_bodies; ++i) {
        x_cm  += mass[i] * bodies.x[i];
        y_cm  += mass[i] * bodies.y[i];
        z_cm  += mass[i] * bodies.z[i];
        vx_cm += mass[i] * bodies.vx[i];
        vy_cm += mass[i] * bodies.vy[i];
        vz_cm += mass[i] * bodies.vz[i];
    }

    x_cm  /= M_total;
    y_cm  /= M_total;
    z_cm  /= M_total;
    vx_cm /= M_total;
    vy_cm /= M_total;
    vz_cm /= M_total;

    for (std::size_t i = 0; i < n_bodies; ++i) {
        bodies.x[i]  -= x_cm;
        bodies.y[i]  -= y_cm;
        bodies.z[i]  -= z_cm;
        bodies.vx[i] -= vx_cm;
        bodies.vy[i] -= vy_cm;
        bodies.vz[i] -= vz_cm;
    }

    // Time integrator.
    Integrator integrator = rk4;

    // Save configuration.
    const std::string directory = "./outputs/galaxy"; // Output directory for the HDF5 files.
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
SetupRegistrar register_galaxy("galaxy", setup_galaxy);