from bodies import Body, System

body1 = Body(1.0, [0, 0], [0, 1])
body2 = Body(1.0, [1, 0], [0, -1])

system = System([body1, body2])

print(body1.mass, body1.position, body1.velocity)
print(system.get_masses())