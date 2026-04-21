#pragma once

#include "solver.hpp"


/**
 * @brief Computes the right-hand side of the N-body ODE system.
 *
 * @param state State variables of the system.
 * @param params Physical parameters.
 * @param mpi_context MPI execution context.
 * @return Right-hand side of the ODE system.
 */
State nbody_rhs(
    const State& state,
    const Params& params,
    const MPIContext& mpi_context
);