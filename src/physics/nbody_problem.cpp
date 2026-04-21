#include "nbody_problem.hpp"

#include <mpi.h>
#include <omp.h>

#include <cmath>


State nbody_rhs(
    const State& state,
    const Params& params,
    const MPIContext& mpi_context
) {
    // Alias the input state for concise mathematical notation.
    const State& U = state;

    // Unpack physical parameters.
    const double G = params.gravitational_constant;
    const double eps = params.softening_factor;
    const std::vector<double>& m = params.masses;

    // Total number of bodies in the simulation.
    const int num_bodies = U.x.size();

    // Initialize the state derivative.
    State dUdt{
        .x = std::vector<double>(num_bodies),
        .y = std::vector<double>(num_bodies),
        .z = std::vector<double>(num_bodies),
        .vx = std::vector<double>(num_bodies),
        .vy = std::vector<double>(num_bodies),
        .vz = std::vector<double>(num_bodies)
    };

    // Local index range handled by this MPI rank.
    const int local_begin = mpi_context.displacements[mpi_context.rank];
    const int local_end = local_begin + mpi_context.counts[mpi_context.rank];

    // Distribute the local body loop across OpenMP threads.
    #pragma omp parallel for
    for (int i = local_begin; i < local_end; i++) {
        // The time derivative of position is velocity.
        dUdt.x[i] = U.vx[i];
        dUdt.y[i] = U.vy[i];
        dUdt.z[i] = U.vz[i];

        // Acceleration for body i.
        double ax = 0.0;
        double ay = 0.0;
        double az = 0.0;

        // Sum gravitational contributions from all other bodies.
        for (int j = 0; j < num_bodies; j++) {
            if (i == j) {
                continue;
            }

            // Relative displacement from body i to body j.
            const double rx = U.x[j] - U.x[i];
            const double ry = U.y[j] - U.y[i];
            const double rz = U.z[j] - U.z[i];

            // Softened inverse-cube distance factor.
            const double r = std::sqrt(rx*rx + ry*ry + rz*rz + eps*eps);
            const double inv_r3 = 1.0/(r*r*r);

            // Add the contribution of body j to the acceleration of body i (Newton's law of universal gravitation).
            ax += G*m[j]*rx*inv_r3;
            ay += G*m[j]*ry*inv_r3;
            az += G*m[j]*rz*inv_r3;
        }

        // The time derivative of velocity is acceleration.
        dUdt.vx[i] = ax;
        dUdt.vy[i] = ay;
        dUdt.vz[i] = az;
    }

    // Rebuild the full derivative on every rank by summing disjoint local contributions.
    MPI_Allreduce(MPI_IN_PLACE, dUdt.x.data(), num_bodies, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);
    MPI_Allreduce(MPI_IN_PLACE, dUdt.y.data(), num_bodies, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);
    MPI_Allreduce(MPI_IN_PLACE, dUdt.z.data(), num_bodies, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);
    MPI_Allreduce(MPI_IN_PLACE, dUdt.vx.data(), num_bodies, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);
    MPI_Allreduce(MPI_IN_PLACE, dUdt.vy.data(), num_bodies, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);
    MPI_Allreduce(MPI_IN_PLACE, dUdt.vz.data(), num_bodies, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);

    return dUdt;
}
