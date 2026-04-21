#pragma once

#include "solver.hpp"

#include <functional>
#include <string>
#include <unordered_map>


/**
 * @brief Function type used to create a simulation from a named setup.
 *
 * Each setup is registered as a function that builds and returns a fully
 * configured Simulation object. These functions are stored in a registry
 * and looked up by name at runtime.
 */
using SetupFunction = std::function<Simulation()>;


/**
 * @brief Returns the global registry of simulation setups.
 *
 * @return Registry of simulation setups indexed by name.
 */
std::unordered_map<std::string, SetupFunction>& setup_registry();


/**
 * @brief Registers a simulation setup in the global registry.
 */
struct SetupRegistrar {
    SetupRegistrar(const std::string& name, SetupFunction setup_function);
};


/**
 * @brief Creates a random N-body simulation setup.
 *
 * @return Simulation struct containing the initial state and all settings.
 */
Simulation setup_random();


/**
 * @brief Creates a galaxy-like N-body simulation setup.
 *
 * @return Simulation struct containing the initial state and all settings.
 */
Simulation setup_galaxy();


/**
 * @brief Creates the three-body figure-eight choreography setup.
 *
 * @return Simulation struct containing the initial state and all settings.
 */
Simulation setup_eight();
