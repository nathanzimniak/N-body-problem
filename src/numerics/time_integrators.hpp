#pragma once

#include "solver.hpp"


/**
 * @brief Advance the simulation state by one explicit Euler time step.
 *
 * @param[in]     rhs    Right-hand side of the governing equations.
 * @param[in,out] U      State variables of the system.
 * @param[in]     dt     Time-step size.
 * @param[in]     params Physical parameters.
 **/
void euler_explicit(
    RHSFunction rhs,
    State& U,
    double dt,
    const Params& params
);


/**
 * @brief Advance the simulation state by one RK4 time step.
 *
 * @param[in]     rhs    Right-hand side of the governing equations.
 * @param[in,out] U      State variables of the system.
 * @param[in]     dt     Time-step size.
 * @param[in]     params Physical parameters.
 **/
void rk4(
    RHSFunction rhs,
    State& U,
    double dt,
    const Params& params
);
