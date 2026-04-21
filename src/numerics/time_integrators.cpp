#include "time_integrators.hpp"


void euler_explicit(
    RHSFunction rhs,
    State& state,
    double timestep,
    const Params& params,
    const MPIContext& mpi_context
) {
    // Alias for concise mathematical notation.
    State& U = state;
    const double dt = timestep;

    // Number of bodies in the simulation.
    const int num_bodies = U.x.size();

    // Compute the slope at the current state.
    const State k1 = rhs(U, params, mpi_context);
    for (int i = 0; i < num_bodies; ++i) {
        U.x[i] += dt*k1.x[i];
        U.y[i] += dt*k1.y[i];
        U.z[i] += dt*k1.z[i];
        U.vx[i] += dt*k1.vx[i];
        U.vy[i] += dt*k1.vy[i];
        U.vz[i] += dt*k1.vz[i];
    }
}


void rk4(
    RHSFunction rhs,
    State& state,
    double timestep,
    const Params& params,
    const MPIContext& mpi_context
) {
    // Alias for concise mathematical notation.
    State& U = state;
    const double dt = timestep;

    // Number of bodies in the simulation.
    const int num_bodies = U.x.size();

    // Preserve the initial state for the RK4 stages.
    const State U0 = U;

    // Stage 1: slope at the beginning of the interval.
    const State k1 = rhs(U, params, mpi_context);
    for (int i = 0; i < num_bodies; ++i) {
        U.x[i] = U0.x[i] + 0.5*dt*k1.x[i];
        U.y[i] = U0.y[i] + 0.5*dt*k1.y[i];
        U.z[i] = U0.z[i] + 0.5*dt*k1.z[i];
        U.vx[i] = U0.vx[i] + 0.5*dt*k1.vx[i];
        U.vy[i] = U0.vy[i] + 0.5*dt*k1.vy[i];
        U.vz[i] = U0.vz[i] + 0.5*dt*k1.vz[i];
    }

    // Stage 2: slope at the midpoint using k1.
    const State k2 = rhs(U, params, mpi_context);
    for (int i = 0; i < num_bodies; ++i) {
        U.x[i] = U0.x[i] + 0.5*dt*k2.x[i];
        U.y[i] = U0.y[i] + 0.5*dt*k2.y[i];
        U.z[i] = U0.z[i] + 0.5*dt*k2.z[i];
        U.vx[i] = U0.vx[i] + 0.5*dt*k2.vx[i];
        U.vy[i] = U0.vy[i] + 0.5*dt*k2.vy[i];
        U.vz[i] = U0.vz[i] + 0.5*dt*k2.vz[i];
    }

    // Stage 3: slope at the midpoint using k2.
    const State k3 = rhs(U, params, mpi_context);
    for (int i = 0; i < num_bodies; ++i) {
        U.x[i] = U0.x[i] + dt*k3.x[i];
        U.y[i] = U0.y[i] + dt*k3.y[i];
        U.z[i] = U0.z[i] + dt*k3.z[i];
        U.vx[i] = U0.vx[i] + dt*k3.vx[i];
        U.vy[i] = U0.vy[i] + dt*k3.vy[i];
        U.vz[i] = U0.vz[i] + dt*k3.vz[i];
    }

    // Stage 4: slope at the end of the interval using k3.
    const State k4 = rhs(U, params, mpi_context);
    for (int i = 0; i < num_bodies; ++i) {
        U.x[i] = U0.x[i] + (dt/6.0)*(k1.x[i] + 2.0*k2.x[i] + 2.0*k3.x[i] + k4.x[i]);
        U.y[i] = U0.y[i] + (dt/6.0)*(k1.y[i] + 2.0*k2.y[i] + 2.0*k3.y[i] + k4.y[i]);
        U.z[i] = U0.z[i] + (dt/6.0)*(k1.z[i] + 2.0*k2.z[i] + 2.0*k3.z[i] + k4.z[i]);
        U.vx[i] = U0.vx[i] + (dt/6.0)*(k1.vx[i] + 2.0*k2.vx[i] + 2.0*k3.vx[i] + k4.vx[i]);
        U.vy[i] = U0.vy[i] + (dt/6.0)*(k1.vy[i] + 2.0*k2.vy[i] + 2.0*k3.vy[i] + k4.vy[i]);
        U.vz[i] = U0.vz[i] + (dt/6.0)*(k1.vz[i] + 2.0*k2.vz[i] + 2.0*k3.vz[i] + k4.vz[i]);
    }
}
