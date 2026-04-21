#pragma once

#include "solver.hpp"


/**
 * @brief Saves the current system state to an HDF5 file.
 *
 * @param state Current state of the system.
 * @param step Current iteration number.
 * @param time Current simulation time.
 * @param output_path Output directory for the HDF5 files.
 */
void save_state_hdf5(
    const State& state,
    int step,
    double time,
    const std::string& output_path
);
