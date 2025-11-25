def euler(t, u, dt, compute_dudt, *args):
    """
    Euler explicite (cohérent avec RK4)
    
    u : état courant
    t : temps courant
    dt : pas de temps
    compute_dudt : fonction dérivée du système (t, u, ...)
    args : paramètres supplémentaires (m, G, ...)
    """

    dudt = compute_dudt(t, u, *args)

    u_new = [ui + dudi*dt for ui, dudi in zip(u, dudt)]
    return u_new


def rk4(t, u, dt, compute_dudt, *args):
    """
    Runge–Kutta 4 (RK4) explicit integrator.

    t : current time
    u : current state vector
    dt : time step
    compute_dudt : function computing du/dt = f(t, u, ...)
    args : additional parameters passed to compute_dudt (m, G, ...)
    """

    # k1
    k1 = compute_dudt(t, u, *args)

    # k2 : t + dt/2, u + dt/2 * k1
    u2 = [ui + 0.5*dt*k1i for ui, k1i in zip(u, k1)]
    k2 = compute_dudt(t + 0.5*dt, u2, *args)

    # k3 : t + dt/2, u + dt/2 * k2
    u3 = [ui + 0.5*dt*k2i for ui, k2i in zip(u, k2)]
    k3 = compute_dudt(t + 0.5*dt, u3, *args)

    # k4 : t + dt, u + dt * k3
    u4 = [ui + dt*k3i for ui, k3i in zip(u, k3)]
    k4 = compute_dudt(t + dt, u4, *args)

    # Combinaison finale
    u_new = [ui + dt/6.0 * (k1i + 2.0*k2i + 2.0*k3i + k4i) for ui, k1i, k2i, k3i, k4i in zip(u, k1, k2, k3, k4)]

    return u_new
