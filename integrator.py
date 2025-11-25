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