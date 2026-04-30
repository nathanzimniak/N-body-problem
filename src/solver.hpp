#pragma once

#include <string>
#include <vector>

/**
 * @brief Stores the full state of an N-body system.
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
 * @brief Stores the physical parameters used by the simulation.
 */
struct Params {
    const double gravitational_constant;
    const double softening_factor;
    const std::vector<double> masses;
};


/**
 * @brief Stores MPI-related execution context.
 */
struct MPIContext {
    const int rank;
    const int size;
};


/**
 * @brief Function pointer type for the right-hand side evaluation.
 */
using RHSFunction = State (*)(const State&, const Params&, const MPIContext&);


/**
 * @brief Function pointer type for the time integrator.
 */
using Integrator = void (*)(RHSFunction, State&, double, const Params&, const MPIContext&);


/**
 * @brief Stores the time parameters used by the simulation.
 */
struct TimeConfig {
    const double start;
    const double end;
    const double step;
};


/**
 * @brief Stores the output parameters.
 */
struct SaveConfig {
    const std::string directory;
    const int frequency;
};


/**
 * @brief Stores all the state and configuration required to run a simulation.
 */
struct Simulation {
    State state;
    const Params params;
    const TimeConfig time;
    const Integrator integrator;
    const SaveConfig save;
};


/**
 * @brief Runs a simulation for the specified setup.
 *
 * @param setup_name Name of the simulation setup to run.
 * @return Exit code: 0 on success, 1 on failure.
 */
int run(const std::string& setup_name);
