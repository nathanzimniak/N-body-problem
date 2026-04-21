#include "solver.hpp"
#include <mpi.h>
#include <iostream>
#include <string>


int main(
    int argc,
    char* argv[]
) {
    // Initialize the MPI execution environment.
    MPI_Init(&argc, &argv);

    // Exit code.
    int exit_code = 0;

    // Setup name (default value can be overridden via CLI).
    std::string setup_name = "random";

    // Iterate over command-line arguments, ignoring argv[0] (program name).
    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];

        // Handle --setup <value>.
        if (arg == "--setup" && i + 1 < argc) {
            i = i + 1;
            setup_name = argv[i];
        }
        else {
            std::cerr << "Unknown argument: " << arg << '\n';
            exit_code = 1;
            break;
        }
    }

    // Run the simulation.
    if (exit_code == 0) {
        exit_code = run(setup_name);
    }

    // Finalize the MPI environment and release associated resources.
    MPI_Finalize();

    return exit_code;
}