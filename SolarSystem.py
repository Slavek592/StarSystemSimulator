from Definitions import System
from Definitions import MapScreen


def go_away(spaceship, system_data):
    if spaceship.fuel > 1:
        for i in [0, 1]:
            spaceship.speed[i] += spaceship.speed[i] / (spaceship.speed[0]**2
                                                        + spaceship.speed[1]**2)**0.5 / 1000000
        spaceship.fuel -= 1
        if spaceship.fuel == 0:
            spaceship.turtle.color("red")


def go_to_mars(spaceship, system_data):
    for planet in system_data.planets:
        if planet.name == "Mars":
            mars = planet.position
            ms = planet.speed
            break
    distance = ((spaceship.position[0] + spaceship.speed[0] - mars[0] - ms[0]) ** 2
                + (spaceship.position[1] + spaceship.speed[1] - mars[1] - ms[1]) ** 2) ** 0.5
    if (distance < 3) and (spaceship.fuel >= 2):
        print("GOGOGO!!!")
        for i in [0, 1]:
            spaceship.speed[i] += (mars[i] + ms[i] - spaceship.position[i] - spaceship.speed[i]) / distance / 50
        spaceship.fuel -= 2


system = System.System()
system.create_from_list([
    ["planet", "Earth", 59.72, 0.006, [0.0, 149.598], [-0.107218, 0.0], "blue"],
    ["star", "Sun", 19885000.0, 0.7, [0.0, 0.0], [-0.00000345, 0.0], 1.0, "yellow"],
    ["planet", "Venus", 48.68, 0.006, [0.0, 108.21], [-0.126072, 0.0], "orange"],
    #["planet", "Moon", 0.73, 0.002, [-0.3844, 149.598], [-0.10721772, -0.0036792], "white"],
    ["planet", "Mars", 6.42, 0.003, [-146.52, 174.61], [-0.0664, -0.0557], "red"],
    #["planet", "Mars", 6.42, 0.003, [0.0, 227.939], [-0.0867, 0.0], "red"],
    #["Comet", 0.0, 0.0, [0.0, 50], [0.3, 0.0]],
    #["Comet", 0.0, 0.0, [0.0, -50], [0.24, 0.0]],
    ["planet", "Mercury", 3.3, 0.002, [57.9, 0], [-0.00000442567, 0.1705], "black"],
    ["planet", "Jupiter", 18982.0, 0.07, [0.0, -778.479], [0.047052, 0.0], "brown"],
    ["planet", "Ceres", 0.0094, 0.001, [0.0, 414.0], [-0.0644, 0.0], "grey"],
    ["planet", "Vesta", 0.0026, 0.0005, [0.0, 353.0], [-0.0696, 0.0], "grey"],
    ["planet", "Saturn", 5684.0, 0.06, [0.0, 1433.53], [-0.034848, 0.0], "yellow"],
    ["spaceship", "Spaceship", 0.0, 0.0, [-0.064, 149.598], [-0.123218, 0.0], go_to_mars, 80000, "green"]
])
spaceship_window = MapScreen.MapWindow(spy_object=system.planets[-1], scale=4)
for planet in system.planets:
    t = spaceship_window.add_turtle()
    t.prepare_turtle(planet.position)
    planet.turtles.append(t)
system.screens.append(spaceship_window)

try:
    while True:
        system.go()
except KeyboardInterrupt:
    system.write()
