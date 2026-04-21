#include "setups.hpp"
#include "solver.hpp"
#include "time_integrators.hpp"

#include <random>


static double random_double(double min, double max) {
    // Create a random number generator.
    static std::mt19937 gen(std::random_device{}());

    // Define a uniform distribution between the requested bounds.
    std::uniform_real_distribution<> dist(min, max);

    return dist(gen);
}


Simulation setup_random() {
    // Total number of bodies in the simulation.
    const int num_bodies = 10000;

    // Physical parameters.
    const double gravitational_constant = 1.0;
    const double softening_factor = 0.1;
    std::vector<double> masses(num_bodies);
    for (int i = 0; i < num_bodies; i++) {
        masses[i] = random_double(0.1, 10.0);
    }

    const Params params{
        .gravitational_constant = gravitational_constant,
        .softening_factor = softening_factor,
        .masses = masses
    };

    // Time parameters.
    const double start_time = 0.0;
    const double end_time = 0.5;
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

    for (int i = 0; i < num_bodies; i++) {
        state.x[i]  = random_double(-2.0, 2.0);
        state.y[i]  = random_double(-2.0, 2.0);
        state.z[i]  = random_double(-2.0, 2.0);
        state.vx[i] = random_double(-2.0, 2.0);
        state.vy[i] = random_double(-2.0, 2.0);
        state.vz[i] = random_double(-2.0, 2.0);
    }

    // Time integrator.
    const Integrator integrator = rk4;

    // Save configuration.
    const std::string output_directory = "./outputs/random";
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
SetupRegistrar register_random("random", setup_random);