#pragma once

#include "solver.hpp"
#include <functional>
#include <string>
#include <unordered_map>


/**
 * @brief Function type used to create a Simulation from a named setup.
 *        Each setup is registered as a function that builds and returns a fully
 *        configured Simulation object. These functions are stored in a registry
 *        and looked up by name at runtime.
 */
using SetupFunction = std::function<Simulation()>;


/**
 * @brief @brief Dictionary of simulation setups.
 */


/**
 * @brief Function to access the global dictionary of simulation setups.
 * 
 * @return Dictionary of simulation setups.
 **/
std::unordered_map<std::string, SetupFunction>& setup_registry();


/**
 * @brief Structure used to register a simulation setup.
 *        The constructor registers a setup function in the global registry.
 */
struct SetupRegistrar {
    SetupRegistrar(const std::string& name, SetupFunction func);
};


/**
 * @brief Function to set up the initial conditions and parameters for a random N-body simulation.
 * 
 * @return Simulation object containing the initial state and all simulation settings.
 **/
Simulation setup_random();


/**
 * @brief Function to set up the initial conditions and parameters for a galaxy-like N-body simulation.
 * 
 * @return Simulation object containing the initial state and all simulation settings.
 **/
Simulation setup_galaxy();


/**
 * @brief Function to set up the initial conditions and parameters for the three-body figure-eight choreography.
 * 
 * @return Simulation object containing the initial state and all simulation settings.
 **/
Simulation setup_eight();
