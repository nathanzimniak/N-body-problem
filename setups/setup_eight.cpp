#include "setups.hpp"
#include "solver.hpp"
#include "time_integrators.hpp"

Simulation setup_eight() {
    // Total number of bodies in the simulation.
    const int num_bodies = 3;

    // Physical parameters.
    const double gravitational_constant = 1.0;
    const double softening_factor = 1e-3;
    const std::vector<double> masses(num_bodies, 1.0);

    const Params params{
        .gravitational_constant = gravitational_constant,
        .softening_factor = softening_factor,
        .masses = masses
    };

    // Time parameters.
    const double start_time = 0.0;
    const double end_time = 20.0;
    const double time_step = 1e-4;

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

    // Standard figure-eight initial conditions (equal-mass three-body choreography).
    state.x[0] = 0.97000436;
    state.y[0] = -0.24308753;
    state.z[0] = 0.0;
    state.vx[0] = 0.4662036850;
    state.vy[0] = 0.4323657300;
    state.vz[0] = 0.0;

    state.x[1] = -0.97000436;
    state.y[1] = 0.24308753;
    state.z[1] = 0.0;
    state.vx[1] = 0.4662036850;
    state.vy[1] = 0.4323657300;
    state.vz[1] = 0.0;

    state.x[2] = 0.0;
    state.y[2] = 0.0;
    state.z[2] = 0.0;
    state.vx[2] = -0.93240737;
    state.vy[2] = -0.86473146;
    state.vz[2] = 0.0;

    // Time integrator.
    const Integrator integrator = rk4;

    // Save configuration.
    const std::string output_directory = "./outputs/eight";
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
SetupRegistrar register_eight("eight", setup_eight);
