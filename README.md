<h2 align="center">N-Body Solver</h2>

<br>

<p align="center">
    A simple <strong>3D gravitational N-body solver</strong> based on <strong>direct force summation</strong> (brute-force).
    <br>
    Written in <strong>C++</strong> using the <strong>OpenMP</strong> API.
</p>

<br>

<p align="center">
    <img src="https://github.com/nathanzimniak/nbody-solver/blob/main/docs/images/banner.png">
</p>

<br>

---

### Physical Model

The solver integrates the Newtonian gravitational N-body equations in three dimensions. A softening parameter is included to prevent numerical divergences during close encounters and improve numerical stability.

---

### Numerical Method

The current implementation relies on direct summation of pairwise gravitational interactions, resulting in an O(N²) computational complexity. While computationally expensive for large numbers of bodies, this approach is robust, simple to implement and extend.

For large simulations, running the code on a HPC cluster is highly recommended.

---

### Getting Started

Clone the repository:

```
git clone https://github.com/nathanzimniak/nbody-solver.git
```

Build the code:

```
make
```

Run a simulation using a setup file from the ```setups/``` directory:

```
OMP_NUM_THREADS=4 ./main --setup galaxy
```

Outputs are saved in **HDF5** format. You can create new simulations by adding configuration files in the ```setups/``` folder.

---

### Contributing

Contributions are welcome. Feel free to open an issue or submit a pull request if you find a bug, or want to implement a new numerical method.
