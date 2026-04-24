#include "setups.hpp"
#include "solver.hpp"
#include "time_integrators.hpp"

#include <cmath>
#include <random>


static double random_double(double min, double max) {
    // Create a random number generator.
    static std::mt19937 gen(std::random_device{}());

    // Define a uniform distribution between the requested bounds.
    std::uniform_real_distribution<> dist(min, max);

    return dist(gen);
}


Simulation setup_galaxy() {
    // Total number of bodies in the simulation.
    const int num_bodies = 10000;

    // Physical parameters.
    const double gravitational_constant = 1.0;
    const double softening_factor = 0.1;
    const std::vector<double> masses(num_bodies, 1.0/num_bodies);

    const Params params{
        .gravitational_constant = gravitational_constant,
        .softening_factor = softening_factor,
        .masses = masses
    };

    // Time parameters.
    const double start_time = 0.0;
    const double end_time = 3.0;
    const double time_step = 1e-3;

    const TimeConfig time{
        .start = start_time,
        .end = end_time,
        .step = time_step
    };

    // Initial conditions.
    State state{
        .x = std::vector<double>(num_bodies),
        .y = std::vector<double>(num_bodies),
        .z = std::vector<double>(num_bodies),
        .vx = std::vector<double>(num_bodies),
        .vy = std::vector<double>(num_bodies),
        .vz = std::vector<double>(num_bodies)
    };

    // Disk scale radius, disk thickness, and radial cutoff.
    const double disk_scale_radius = 2.0;
    const double disk_half_thickness = 0.08;
    const double max_radius = 10.0;
    constexpr double pi = 3.14159265358979323846;

    // Total mass.
    double total_mass = 0.0;
    for (int i = 0; i < num_bodies; i++) {
        total_mass += masses[i];
    }

    // Generate disk-like initial conditions.
    for (int i = 0; i < num_bodies; i++) {
        // Sample a radius from an exponential disk with rejection beyond max_radius.
        double radius = 0.0;
        while (true) {
            const double u = random_double(0.0, 1.0);
            radius = -disk_scale_radius * std::log(1.0 - u);
            if (radius < max_radius) {
                break;
            }
        }

        const double phi = random_double(0.0, 2.0 * pi);

        // m = 2 perturbation to seed non-axisymmetric structure.
        const double perturbation = 1.0 + 0.05 * std::cos(2.0 * phi);

        // Thin-disk geometry.
        state.x[i] = perturbation * radius * std::cos(phi);
        state.y[i] = perturbation * radius * std::sin(phi);
        state.z[i] = random_double(-disk_half_thickness, disk_half_thickness);

        // Simple enclosed-mass model for a disk-like rotation curve.
        const double enclosed_mass =
            total_mass * (1.0 - std::exp(-radius / disk_scale_radius) * (1.0 + radius / disk_scale_radius));

        // Circular speed.
        const double circular_speed =
            std::sqrt(gravitational_constant * enclosed_mass / std::max(radius, 1e-3));

        // Add a small velocity dispersion to seed spiral structure.
        const double radial_dispersion = 0.04 * circular_speed;
        const double azimuthal_dispersion = 0.025 * circular_speed;
        const double vertical_dispersion = 0.012 * circular_speed;

        // Polar basis vectors in the disk plane.
        const double radial_x = std::cos(phi);
        const double radial_y = std::sin(phi);
        const double azimuthal_x = -std::sin(phi);
        const double azimuthal_y = std::cos(phi);

        // Small spiral seed in azimuthal velocity.
        const double spiral_seed = 1.0 + 0.05 * std::cos(2.0 * phi);

        const double radial_velocity = random_double(-radial_dispersion, radial_dispersion);
        const double azimuthal_velocity =
            circular_speed * spiral_seed + random_double(-azimuthal_dispersion, azimuthal_dispersion);
        const double vertical_velocity = random_double(-vertical_dispersion, vertical_dispersion);

        state.vx[i] = radial_velocity * radial_x + azimuthal_velocity * azimuthal_x;
        state.vy[i] = radial_velocity * radial_y + azimuthal_velocity * azimuthal_y;
        state.vz[i] = vertical_velocity;
    }

    // Compute the center-of-mass position and velocity.
    double x_cm = 0.0;
    double y_cm = 0.0;
    double z_cm = 0.0;
    double vx_cm = 0.0;
    double vy_cm = 0.0;
    double vz_cm = 0.0;

    for (int i = 0; i < num_bodies; i++) {
        x_cm += masses[i] * state.x[i];
        y_cm += masses[i] * state.y[i];
        z_cm += masses[i] * state.z[i];
        vx_cm += masses[i] * state.vx[i];
        vy_cm += masses[i] * state.vy[i];
        vz_cm += masses[i] * state.vz[i];
    }

    x_cm /= total_mass;
    y_cm /= total_mass;
    z_cm /= total_mass;
    vx_cm /= total_mass;
    vy_cm /= total_mass;
    vz_cm /= total_mass;

    // Shift to the center-of-mass frame.
    for (int i = 0; i < num_bodies; i++) {
        state.x[i] -= x_cm;
        state.y[i] -= y_cm;
        state.z[i] -= z_cm;
        state.vx[i] -= vx_cm;
        state.vy[i] -= vy_cm;
        state.vz[i] -= vz_cm;
    }

    // Time integrator.
    const Integrator integrator = rk4;

    // Save configuration.
    const std::string output_directory = "./outputs/galaxy";
    const int save_frequency = 50;

    const SaveConfig save{
        .directory = output_directory,
        .frequency = save_frequency
    };

    return Simulation{
        .state = state,
        .params = params,
        .time = time,
        .integrator = integrator,
        .save = save,
    };
}

// Register the setup in the global registry at program startup.
SetupRegistrar register_galaxy("galaxy", setup_galaxy);
