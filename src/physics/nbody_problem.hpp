#pragma once

#include "solver.hpp"


/**
 * @brief Function to compute the RHS of the n-body problem ODE system.
 *
 * @param[in] U      State variables of the system.
 * @param[in] params Physical parameters.
 * 
 * @return dUdt      RHS of the ODE system.
 */
State nbody_rhs(
    const State& U,
    const Params& params
);
