### The 3D N-body problem

This project numerically integrates the equations of motion for multiple bodies in three-dimensional space. It includes ready-to-run presets for the inner solar system and a three-body choreography example, and can be extended with custom initial conditions.
 
<p align='center'>
    <br/>
      <img src="https://raw.githubusercontent.com/nathanzimniak/N-body-problem/main/visualization/inner_solar_system_frames/animation.gif" width="200" height="200"/>
      <img src="https://raw.githubusercontent.com/nathanzimniak/N-body-problem/main/visualization/three_body_orbits/animation.gif" width="200" height="200"/>
    <br/>
 </p>
 
#### PROJECT STRUCTURE
- `src/main.py`: entry point that loads a preset, integrates the system using a solver, and writes trajectories to CSV.
- `src/init.py`: predefined presets (`inner_solar_system`, `three_body_orbits`) and a loader for custom configurations.
- `src/integrator.py`: integrators that can be used to integrate the system.
- `src/rhs.py`: the right-hand side (the derivatives) to integrate.
- `src/accelerations.py`: the accelerations used in the right-hand side.
- `src/bodies.py`: classes representing bodies and systems.
- `outputs/`: CSV outputs produced by simulations.
- `visualization/`: Blender template/script and example animations.

In practice, `main.py` loads a preset from `init.py` and builds the arrays of initial masses, positions, and velocities. At each step, an integrator from `integrator.py` advances positions and velocities by evaluating the derivative via `compute_dudt()` in `rhs.py` (which calls `compute_accelerations()` to compute each body's acceleration via Newton's law of universal gravitation). Each state is added to a global trajectory, converted to `(t, body_id, x, y, z)` rows, and exported as CSV in `outputs/`, ready for visualization or animation with the Blender scripts in `visualization/`.

#### REQUIREMENTS
- Python (with the standard library)
- Blender and FFMPEG (only for visualization)

#### RUNNING A SIMULATION
1. Ensure you are in the repository root.
2. Select a preset in `src/main.py` by setting `preset = "inner_solar_system"` or `preset = "three_body_orbits"`.
3. Run the simulation:
   ```bash
   python src/main.py
   ```
4. View the generated CSV at `outputs/<preset>.csv`. Each row contains the timestamp, body index, and 3D position for every step.

#### CREATING A NEW PRESET
1. Open `src/init.py` and add a new function that returns a dictionary with `t_ini`, `t_end`, `N_steps`, `masses`, `positions`, and `velocities`.
2. Register the function in the `AVAILABLE_PRESETS` dictionary.
3. Set `preset` in `src/main.py` to your new key and run the simulation.
