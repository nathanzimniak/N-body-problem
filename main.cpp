#include "solver.hpp"

#include <iostream>
#include <string>


int main(
    int argc,
    char* argv[]
) {
    // Declare setup name with default value (can be overridden via CLI).
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
            return 1;
        }
    }

    // Run the simulation.
    int result = run(setup_name);

    return result;
}