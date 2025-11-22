from bodies import Body, System
from accelerations import compute_accelerations



def compute_dfdt(t, f, m, G):
    # Unpack state vector
    x1, y1, vx1, vy1, x2, y2, vx2, vy2 = f

    # Compute accelerations with current system state
    positions = [[x1, y1], [x2, y2]]
    accelerations = compute_accelerations(positions, m, G)
    ax1, ay1 = accelerations[0]
    ax2, ay2 = accelerations[1]

    # Build dfdt
    dfdt1 = vx1  # dx1/dt
    dfdt2 = vy1  # dy1/dt
    dfdt3 = ax1  # dvx1/dt
    dfdt4 = ay1  # dvy1/dt
    dfdt5 = vx2  # dx2/dt
    dfdt6 = vy2  # dy2/dt
    dfdt7 = ax2  # dvx2/dt
    dfdt8 = ay2  # dvy2/dt
    dfdt = [dfdt1, dfdt2, dfdt3, dfdt4, dfdt5, dfdt6, dfdt7, dfdt8]
    return dfdt

def euler(f, dfdt, dt):
    f1, f2, f3, f4, f5, f6, f7, f8 = f
    dfdt1, dfdt2, dfdt3, dfdt4, dfdt5, dfdt6, dfdt7, dfdt8 = dfdt

    f1 = f1 + dfdt1 * dt
    f2 = f2 + dfdt2 * dt
    f3 = f3 + dfdt3 * dt
    f4 = f4 + dfdt4 * dt
    f5 = f5 + dfdt5 * dt
    f6 = f6 + dfdt6 * dt
    f7 = f7 + dfdt7 * dt
    f8 = f8 + dfdt8 * dt
    f = [f1, f2, f3, f4, f5, f6, f7, f8]
    return f




G = 1.0

# Input parameters
t_ini, t_end, N_steps = [0.0, 10.0, 1000]
m1, x1, y1, vx1, vy1 = [1.0, 0.0, 0.0, 0.0, 1.0]
m2, x2, y2, vx2, vy2 = [1.0, 1.0, 0.0, 0.0, -1.0]

# Create the initial system state
body1 = Body(m1, [x1, y1], [vx1, vy1])
body2 = Body(m2, [x2, y2], [vx2, vy2])
system = System([body1, body2])

t = t_ini
dt = (t_end - t_ini)/N_steps

# États actuels
f = [x1, y1, vx1, vy1, x2, y2, vx2, vy2]
m = [m1, m2]

for step in range(N_steps):

    # Calcul des dérivées (rhs)
    dfdt = compute_dfdt(t, f, m, G)

    # Intégration
    f = euler(f, dfdt, dt)
    x1, y1, vx1, vy1, x2, y2, vx2, vy2 = f

    # Mise à jour des positions et vitesses des corps
    body1.position = [x1, y1]
    body1.velocity = [vx1, vy1]
    body2.position = [x2, y2]
    body2.velocity = [vx2, vy2]

    # Incrémentation du temps
    t += dt







## Input parameters
#t_end = 10
#N_steps = 100
#m1, x1, y1, vx1, vy1 = [1.0, 0.0, 0.0, 0.0, 1.0]
#m2, x2, y2, vx2, vy2 = [1.0, 1.0, 0.0, 0.0, -1.0]
#
## Initial states
#Y0 = [x1, y1, vx1, vy1, x2, y2, vx2, vy2]
#M0 = [m1, m2]
#
## Temps d'intégration
#T = np.linspace(0, t_end, N_steps)
#
#def rhs(Y, t, M, G):
#    """
#    Right-hand side of the ODE system for 2 bodies:
#    Y = [x1, y1, vx1, vy1, x2, y2, vx2, vy2]
#    dY/dt = [vx1, vy1, ax1, ay1, vx2, vy2, ax2, ay2]
#    """
#
#    # Unpack state vector and create bodies
#    x1, y1, vx1, vy1, x2, y2, vx2, vy2 = Y
#    m1, m2 = M
#
#    # Create the current system state
#    b1 = Body(m1, [x1, y1], [vx1, vy1])
#    b2 = Body(m2, [x2, y2], [vx2, vy2])
#
#    # Create the current system state
#    system = System([b1, b2])
#
#    # Compute accelerations with current system state
#    accelerations = compute_accelerations(system, G)
#    ax1, ay1 = accelerations[0]
#    ax2, ay2 = accelerations[1]
#
#    # Build dY/dt
#    dydt1 = vx1 # dx1/dt
#    dydt2 = vy1 # dy1/dt
#    dydt3 = ax1 # dvx1/dt
#    dydt4 = ay1 # dvy1/dt
#    dydt5 = vx2 # dx2/dt
#    dydt6 = vy2 # dy2/dt
#    dydt7 = ax2 # dvx2/dt
#    dydt8 = ay2 # dvy2/dt
#    dYdt = [dydt1, dydt2, dydt3, dydt4, dydt5, dydt6, dydt7, dydt8]
#    return dYdt
#
#solution = odeint(rhs, Y0, T, args=(M0, G))
