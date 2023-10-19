from Definitions.System import System
from Definitions.Planet import *
from Definitions.Writer import FileWriter
from Definitions.MapScreen import *

#system = System(FileWriter("TestSystem.txt"))
system = System()
window = MapWindow(offset=[-500, 200])
system.screens.append(window)
window2 = MapWindow(scale=0.5, offset=[-150, 100])
system.screens.append(window2)
alpha = Star(system, "Alpha", 12000000, 0.6, [0.0, 20.0], [0.06, 0.0], 0.65,
             [window.add_turtle(), window2.add_turtle()], "yellow")
beta = Star(system, "Beta", 6000000, 0.5, [0.0, -20.0], [-0.09, 0.0], 0.25,
            [window.add_turtle(), window2.add_turtle()], "orange")
center = MassCenter(system, "Alpha-Beta", 0.0, 0.0, [0.0, 0.0], [0.0, 0.0], [alpha, beta])
window2.spy_object = center
system.add_planets([
    alpha,
    beta,
    center,
    Planet(system, "Earth", 59.7, 0.006, [0.0, 150.0], [-0.1, 0.0], [window.add_turtle(), window2.add_turtle()], "blue"),
    Planet(system, "Venus", 48.68, 0.006, [0.0, 109.0], [-0.13, 0.0], [window.add_turtle(), window2.add_turtle()], "brown"),
    Planet(system, "Mercury", 3.3, 0.002, [57.9, 0.0], [0.0, 0.1705], [window.add_turtle(), window2.add_turtle()], "black"),
    Planet(system, "Mars", 6.42, 0.003, [0.0, 227.939], [-0.075, 0.0], [window.add_turtle(), window2.add_turtle()], "red"),
    Star(system, "Jupiter", 3000000, 0.4, [0.0, -400.0], [-0.06, 0.0], 0.1, [window.add_turtle(), window2.add_turtle()], "orange"),
    Planet(system, "Ganymede", 3.0, 0.003, [-10.0, -400.0], [-0.06, 0.1705], [window.add_turtle(), window2.add_turtle()], "grey"),
    Planet(system, "Saturn", 6000.0, 0.003, [0.0, -800.0], [0.05, 0.0], [window.add_turtle(), window2.add_turtle()], "yellow"),
    Object(system, "Rock", 1.0, 0.002, [0.0, -700.0], [0.0, 0.0], [window.add_turtle(), window2.add_turtle()], "black")
])

try:
    while True:
        system.go()
except KeyboardInterrupt:
    system.write()
