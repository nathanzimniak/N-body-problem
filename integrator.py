

def euler(u, dudt, dt):
    u_new = [ui + dudi*dt for ui, dudi in zip(u, dudt)]
    return u_new