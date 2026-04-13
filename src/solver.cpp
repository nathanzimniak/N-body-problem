#include "solver.hpp"
#include "setups.hpp"
#include "nbody_problem.hpp"
#include "io.hpp"

#include <iostream>
#include <iomanip>
#include <chrono>


std::unordered_map<std::string, SetupFunction>& setup_registry() {
    static std::unordered_map<std::string, SetupFunction> registry;
    return registry;
}


SetupRegistrar::SetupRegistrar(const std::string& name, SetupFunction func) {
    setup_registry()[name] = func;
}


int run(const std::string& setup_name) {

    // Start measuring time.
    auto start = std::chrono::high_resolution_clock::now();

    // Look up the requested setup in the global registry.
    auto& registry = setup_registry();
    auto setup_entry = registry.find(setup_name);

    // Stop if the requested setup is not registered.
    if (setup_entry == registry.end()) {
        std::cerr << "Unknown setup: " << setup_name << '\n';
        return 1;
    }

    // Extract setup function from registry.
    SetupFunction setup_function = setup_entry->second;

    // Build simulation using selected setup.
    Simulation sim = setup_function();

    // Initialize time and iteration counter.
    double t = sim.time.t_start;
    int n = 0;

    // Time integration loop.
    while (t <= sim.time.t_end) {

        // Compute elapsed wall-clock time and simulation progress.
        auto now = std::chrono::high_resolution_clock::now();
        double elapsed = std::chrono::duration<double>(now - start).count();
        double progress = (t - sim.time.t_start)/(sim.time.t_end - sim.time.t_start);

        // Display current iteration, progress, and elapsed time.
        std::cout << std::fixed
                  << "Iteration " << std::setw(6) << n
                  << " | Progress " << std::setprecision(1) << (100.0 * progress) << "%"
                  << " | Elapsed time " << std::setprecision(1) << elapsed << " s"
                  << "\r" << std::flush;

        // Save the simulation state at the configured frequency.
        if (n % sim.save.frequency == 0) {
            save_state_hdf5(sim.bodies, n, t, sim.save.directory);
        }

        // Advance the simulation by one time step.
        sim.integrator(nbody_rhs, sim.bodies, sim.time.dt, sim.params);

        // Update time and iteration counter.
        t += sim.time.dt;
        n++;
    }

    std::cout << std::endl;
    return 0;
}
