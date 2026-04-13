#include "nbody_problem.hpp"

#include <omp.h>
#include <cmath>


State nbody_rhs(
    const State& U,
    const Params& params
) {
    // Unpacking parameters.
    const double G = params.G;
    const double eps = params.eps;
    const std::vector<double>& mass = params.mass;

    // Number of bodies in the simulation.
    const std::size_t N = U.x.size();

    // Initialize the derivative of the state.
    State dUdt {.x  = std::vector<double>(N),
                .y  = std::vector<double>(N),
                .z  = std::vector<double>(N),
                .vx = std::vector<double>(N),
                .vy = std::vector<double>(N),
                .vz = std::vector<double>(N)};

	// Create a team of threads and split the loop iterations among the threads.
    #pragma omp parallel for
    
    // Loop over each body to compute its time derivative.
    for (std::size_t i = 0; i < N; ++i){

        // The time derivative of the position is the velocity.
        dUdt.x[i] = U.vx[i];
        dUdt.y[i] = U.vy[i];
        dUdt.z[i] = U.vz[i];

        // Initialize the acceleration of the current body to zero.
        double ax = 0.0;
        double ay = 0.0;
        double az = 0.0;

        // Compute the acceleration of body i due to the gravitational forces from all other bodies.
        for (std::size_t j = 0; j < N; ++j) {
            if (i == j) continue;

            // Compute the distance between bodies i and j.
            double deltax = U.x[j] - U.x[i];
            double deltay = U.y[j] - U.y[i];
            double deltaz = U.z[j] - U.z[i];

            // Compute the gravitational acceleration using Newton's law of universal gravitation.
            double r = std::sqrt(deltax*deltax + deltay*deltay + deltaz*deltaz + eps*eps);
            double inv_r3 = 1.0/(r*r*r);

            // Update the acceleration of body i due to the gravitational force from body j.
            ax += G * mass[j] * deltax * inv_r3;
            ay += G * mass[j] * deltay * inv_r3;
            az += G * mass[j] * deltaz * inv_r3;
        }

        // The time derivative of the velocity is the acceleration.
        dUdt.vx[i] = ax;
        dUdt.vy[i] = ay;
        dUdt.vz[i] = az; 
    }

    return dUdt;
}
