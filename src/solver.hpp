#pragma once

#include <vector>
#include <string>


/**
 * @brief Structure for the state of an N-body system.
 */
struct State {
    std::vector<double> x;
    std::vector<double> y;
    std::vector<double> z;
    std::vector<double> vx;
    std::vector<double> vy;
    std::vector<double> vz;
};


/**
 * @brief Structure for the physical parameters.
 */
struct Params {
    double G;
    double eps;
    std::vector<double> mass;
};


/**
 * @brief Structure for the MPI context.
 */
struct MPIContext {
    int rank;
    int size;
    std::vector<int> counts;
    std::vector<int> displs;
};


/**
 * @brief Function pointer types for the RHS and integrator functions.
 */
using RHSFunction = State (*)(const State&, const Params&, const MPIContext&);
using Integrator = void (*)(RHSFunction, State&, double, const Params&, const MPIContext&);


/**
 * @brief Structure for the time configuration.
 */
struct TimeConfig {
    double t_start;
    double t_end;
    double dt;
};


/**
 * @brief Structure for the save configuration.
 */
struct SaveConfig {
    std::string directory;
    int frequency;
};


/**
 * @brief Structure to hold the entire simulation configuration.
 */
struct Simulation {
    State bodies;
    Params params;
    TimeConfig time;
    Integrator integrator;
    SaveConfig save;
};


/**
 * @brief Function to run a simulation.
 *
 * @param[in] setup_name Name of the setup to run.
 * 
 * @return 0/1 Exit code.
 */
int run(
    const std::string& setup_name
);