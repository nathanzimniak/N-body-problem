diff --git a/README.md b/README.md
index 7d276bcfaaf82bddb65271670b0efba993b12c00..1f2743f9289cd95ec0933602f5e2ef7053fa19a0 100644
--- a/README.md
+++ b/README.md
@@ -1,14 +1,39 @@
-Solving the 3D N-body problem
-==================================
+# Solving the 3D N-body problem
 
 <p align='center'>
   <br/>
     <img src="https://raw.githubusercontent.com/nathanzimniak/N-body-problem/main/visualization/inner_solar_system_frames/animation.gif" width="200" height="200"/>
     <img src="https://raw.githubusercontent.com/nathanzimniak/N-body-problem/main/visualization/three_body_orbits/animation.gif" width="200" height="200"/>
   <br/>
 </p>
 
-About
------
+This project numerically integrates the equations of motion for multiple bodies in three-dimensional space. It includes ready-to-run presets for the inner solar system and a three-body choreography example, and can be extended with custom initial conditions.
 
-WIP.
+## Project structure
+- `src/main.py` – entry point that loads a preset, integrates the system using a Runge–Kutta solver, and writes trajectories to CSV.
+- `src/init.py` – predefined presets (`inner_solar_system`, `three_body_orbits`) and a loader for custom configurations.
+- `src/integrator.py`, `src/rhs.py`, `src/accelerations.py` – numerical integration routines and derivative calculations.
+- `src/bodies.py` – lightweight classes representing bodies and systems.
+- `outputs/` – CSV outputs produced by simulations (created automatically).
+- `visualization/` – example animations generated from the sample presets.
+
+## Requirements
+- Python 3.8+ (uses only the standard library)
+
+## Running a simulation
+1. Ensure you are in the repository root.
+2. Select a preset in `src/main.py` by setting `preset = "inner_solar_system"` or `preset = "three_body_orbits"`.
+3. Run the simulation:
+   ```bash
+   python src/main.py
+   ```
+4. View the generated CSV at `outputs/<preset>.csv`. Each row contains the timestamp, body index, and 3D position for every step.
+
+## Creating a new preset
+1. Open `src/init.py` and add a new function that returns a dictionary with `t_ini`, `t_end`, `N_steps`, `masses`, `positions`, and `velocities`.
+2. Register the function in the `AVAILABLE_PRESETS` dictionary.
+3. Set `preset` in `src/main.py` to your new key and run the simulation.
+
+## Notes
+- Gravitational constant `G` is expressed in astronomical units with years as the time unit (`G = 4π²`).
+- The default time step is derived from the configured start/end times and number of steps; adjust `N_steps` for accuracy vs. runtime.
