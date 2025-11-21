from bodies import Body, System
from accelerations import compute_accelerations

G = 1.0

body1 = Body(1.0, [0, 0], [0, 1])
body2 = Body(1.0, [1, 0], [0, -1])

system = System([body1, body2])

accelerations = compute_accelerations(system, G)

print(accelerations)