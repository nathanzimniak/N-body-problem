#pragma once

#include "solver.hpp"


/**
 * @brief Advances the simulation state by one explicit Euler time step.
 *
 * @param rhs Right-hand side of the governing equations.
 * @param state State variables of the system.
 * @param timestep Time step size.
 * @param params Physical parameters.
 * @param mpi_context MPI execution context.
 */
void euler_explicit(
    RHSFunction rhs,
    State& state,
    double timestep,
    const Params& params,
    const MPIContext& mpi_context
);


/**
 * @brief Advances the simulation state by one Runge-Kutta 4 time step.
 *
 * @param rhs Right-hand side of the governing equations.
 * @param state State variables of the system.
 * @param timestep Time step size.
 * @param params Physical parameters.
 * @param mpi_context MPI execution context.
 */
void rk4(
    RHSFunction rhs,
    State& state,
    double timestep,
    const Params& params,
    const MPIContext& mpi_context
);
