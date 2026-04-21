#include "solver.hpp"
#include "setups.hpp"
#include "nbody_problem.hpp"
#include "io.hpp"
#include <mpi.h>
#include <iostream>
#include <iomanip>


std::unordered_map<std::string, SetupFunction>& setup_registry() {
    static std::unordered_map<std::string, SetupFunction> registry;
    return registry;
}


SetupRegistrar::SetupRegistrar(const std::string& name, SetupFunction func) {
    setup_registry()[name] = func;
}


int run(
    const std::string& setup_name
) {
    // Start wall-clock timing.
    MPI_Barrier(MPI_COMM_WORLD);
    double start = MPI_Wtime();

    // Total number of processes in the global communicator.
    int size;
    MPI_Comm_size(MPI_COMM_WORLD, &size);

	// Process rank.
	int rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    // Look up the requested setup in the global registry.
    auto& registry = setup_registry();
    auto setup_entry = registry.find(setup_name);

    // Stop if the requested setup is not registered.
    if (setup_entry == registry.end()) {
        if (rank == 0) {
            std::cerr << "Unknown setup: " << setup_name << '\n';
        }
        return 1;
    }

    // Extract setup function from registry.
    SetupFunction setup_function = setup_entry->second;

    // Build simulation using selected setup.
    Simulation sim = setup_function();

    // Number of bodies in the simulation.
    const std::size_t N = sim.bodies.x.size();







    //
    std::vector<int> counts(size), displs(size);

    for (int r = 0; r < size; ++r) {
        counts[r] = N / size + (r < (N % size) ? 1 : 0);
    }

    displs[0] = 0;
    for (int r = 1; r < size; ++r) {
        displs[r] = displs[r - 1] + counts[r - 1];
    }

    // Contexte MPI explicite (Option A)
    MPIContext mpi_ctx{
        .rank = rank,
        .size = size,
        .counts = counts,
        .displs = displs
    };
    //





    // Time and iteration counter.
    double t = sim.time.t_start;
    int n = 0;

    // Time integration loop.
    while (t <= sim.time.t_end) {

        // Compute elapsed wall-clock time and simulation progress.
        double now = MPI_Wtime();
        double elapsed = (now - start);
        double progress = (t - sim.time.t_start)/(sim.time.t_end - sim.time.t_start);

	    if (rank == 0) {
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

	    }

        // Advance the simulation by one time step.
        sim.integrator(nbody_rhs, sim.bodies, sim.time.dt, sim.params, mpi_ctx);

        // Update time and iteration counter.
        t += sim.time.dt;
        n++;
    }

    // Print a final newline once (root process only) to end the progress line cleanly.
	if (rank == 0) {
        std::cout << std::endl;
	}
    
    return 0;
}
