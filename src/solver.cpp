#include "io.hpp"
#include "nbody_problem.hpp"
#include "setups.hpp"
#include "solver.hpp"

#include <mpi.h>

#include <iomanip>
#include <iostream>
#include <unordered_map>
#include <vector>


std::unordered_map<std::string, SetupFunction>& setup_registry() {
    static std::unordered_map<std::string, SetupFunction> registry;
    return registry;
}


SetupRegistrar::SetupRegistrar(const std::string& name, SetupFunction func) {
    setup_registry()[name] = func;
}


int run(const std::string& setup_name) {
    // Synchronize all processes before starting the timer.
    MPI_Barrier(MPI_COMM_WORLD);

    // Start wall-clock timing.
    const double start_wtime = MPI_Wtime();

    // Get total number of processes and current process rank.
    int num_proc;
    int rank_proc;
    MPI_Comm_size(MPI_COMM_WORLD, &num_proc);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank_proc);

    // Find the requested simulation setup in the global registry.
    auto& registry = setup_registry();
    const auto setup_iterator = registry.find(setup_name);

    // Stop if the setup name is not registered.
    if (setup_iterator == registry.end()) {
        if (rank_proc == 0) {
            std::cerr << "Unknown setup: " << setup_name << '\n';
        }
        return 1;
    }

    // Create the simulation from the selected setup function.
    const SetupFunction setup_function = setup_iterator->second;
    Simulation sim = setup_function();

    // Total number of bodies in the simulation.
    const int num_bodies = sim.state.x.size();

    // Number of bodies handled by each process.
    std::vector<int> counts(num_proc);
    for (int rank = 0; rank < num_proc; ++rank) {
        counts[rank] = num_bodies / num_proc + (rank < (num_bodies % num_proc) ? 1 : 0);
    }

    // Starting index (offset) of each process's data in the global array.
    std::vector<int> displacements(num_proc);
    displacements[0] = 0;
    for (int rank = 1; rank < num_proc; ++rank) {
        displacements[rank] = displacements[rank - 1] + counts[rank - 1];
    }

    // MPI distribution metadata for domain decomposition.
    const MPIContext mpi_context{
        .rank = rank_proc,
        .size = num_proc,
        .counts = counts,
        .displacements = displacements
    };

    // Simulation time and iteration counter.
    double current_time = sim.time.start;
    int current_step = 0;

    // Main time integration loop.
    while (current_time <= sim.time.end) {
        // Elapsed wall-clock time and simulation progress.
        const double current_wtime = MPI_Wtime();
        const double elapsed_wtime = current_wtime - start_wtime;
        const double progress = (current_time - sim.time.start)/(sim.time.end - sim.time.start);
    
        if (rank_proc == 0) {
            // Display current iteration, progress, and elapsed wall-clock time.
            std::cout << std::fixed
                      << "Iteration " << std::setw(6) << current_step
                      << " | Progress " << std::setprecision(1) << (100.0 * progress) << "%"
                      << " | Elapsed time " << std::setprecision(1) << elapsed_wtime << " s"
                      << '\n';

            // Save the simulation state at the configured interval.
            if (current_step % sim.save.frequency == 0) {
                save_state_hdf5(sim.state, current_step, current_time, sim.save.directory);
            }
        }

        // Advance the simulation by one time step.
        sim.integrator(nbody_rhs, sim.state, sim.time.step, sim.params, mpi_context);

        // Update simulation time and iteration count.
        current_time += sim.time.step;
        current_step++;
    }
    
    return 0;
}
