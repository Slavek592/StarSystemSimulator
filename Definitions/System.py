from .Planet import *
from .Writer import *
from .MapScreen import *


class System:
    def __init__(self, period=60, writer=NullWriter()):
        self.planets = []
        self.time = 0
        self.period = period
        self.writer = writer
        self.screens = []
        self.collisions = []

    def add_screen(self, offset=[-150, 100], scale=1, angle=0, spy_object=None):
        screen = MapWindow("Simulator", "640x480", offset, scale, angle, spy_object)
        self.screens.append(screen)
        return screen

    def add_planets(self, planets):
        for planet in planets:
            self.planets.append(planet)
            self.writer.write(planet.name + ":[x,y],[sx,sy],[ax,ay],T,")
        self.writer.write("\n")

    def create_from_list(self, planets):
        if len(self.screens) == 0:
            screen = self.add_screen()
        else:
            screen = self.screens[0]
        for planet in planets:
            if planet[0] == "planet":
                if len(planet) > 6:
                    self.planets.append(Planet(
                        self, planet[1], planet[2], planet[3], planet[4], planet[5],
                        [screen.add_turtle()], planet[6]))
                else:
                    self.planets.append(Planet(
                        self, planet[1], planet[2], planet[3], planet[4], planet[5], [screen.add_turtle()]))
            elif planet[0] == "star":
                if len(planet) > 7:
                    self.planets.append(Star(
                        self, planet[1], planet[2], planet[3], planet[4], planet[5],
                        planet[6], [screen.add_turtle()], planet[7]))
                else:
                    self.planets.append(Star(
                        self, planet[1], planet[2], planet[3], planet[4], planet[5],
                        planet[6], [screen.add_turtle()]))
            elif planet[0] == "spaceship":
                if len(planet) > 8:
                    self.planets.append(Spaceship(
                        self, planet[1], planet[2], planet[3], planet[4], planet[5],
                        planet[6], planet[7], [screen.add_turtle()], planet[8]))
                else:
                    self.planets.append(Spaceship(
                        self, planet[1], planet[2], planet[3], planet[4], planet[5],
                        planet[6], planet[7], [screen.add_turtle()]))
            else:
                if len(planet) > 6:
                    self.planets.append(Object(
                        self, planet[1], planet[2], planet[3], planet[4], planet[5],
                        [screen.add_turtle()], planet[6]))
                else:
                    self.planets.append(Object(
                        self, planet[1], planet[2], planet[3], planet[4], planet[5], [screen.add_turtle()]))
            self.writer.write(planet[1] + ":[x,y],[sx,sy],[ax,ay],T,")
        self.writer.write("\n")

    def go(self):
        self.time += 1
        for planet in self.planets:
            planet.move()
        if self.time % self.period == 0:
            for screen in self.screens:
                screen.change_offset()
            for planet in self.planets:
                planet.draw()
                self.writer.write(planet.name + ":" + str(planet.position) + "," + str(planet.speed)
                                  + "," + str(planet.accelerate()) + "," + str(planet.warm_up()) + ",")
            self.writer.write("\n")
        else:
            for planet in self.planets:
                planet.accelerate()
        if len(self.collisions) > 0:
            for collision in self.collisions:
                collision[0].eat_object(collision[1])
                for map_turtle in collision[1].turtles:
                    map_turtle.turtle.shapesize(0.01, 0.01)
                self.planets.remove(collision[1])
            self.collisions = []

    def write(self):
        for planet in self.planets:
            planet.write()
