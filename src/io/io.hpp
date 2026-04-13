#pragma once

#include "solver.hpp"


/**
 * @brief Save the current state of the system to an HDF5 file.
 *
 * @param[in] U    Current state of the system.
 * @param[in] step Current iteration number.
 * @param[in] t    Current time.
 * @param[in] path Output directory for the HDF5 files.
 */
void save_state_hdf5(
    const State& U,
    int step,
    double t,
    const std::string& path
);
