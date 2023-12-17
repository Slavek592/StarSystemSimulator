class Object:
    def __init__(self, system, name, mass, radius, position, speed,
                 turtles=None, color=None):
        if turtles is None:
            turtles = []
        self.system = system
        self.name = name
        self.mass = mass
        self.radius = radius
        self.position = position
        self.speed = speed
        self.turtles = turtles
        self.prepare_turtles(color)
        
    def prepare_turtles(self, color=None):
        for map_turtle in self.turtles:
            map_turtle.prepare_turtle(self.position, color)

    def move(self):
        for i in [0, 1]:
            self.position[i] += self.speed[i]
        # return self.position

    def draw(self):
        for map_turtle in self.turtles:
            map_turtle.go_to_position(self.position)

    def write(self):
        print(self.name + "'s mass: " + str(self.mass))
        print(self.name + "'s position: " + str(self.position))
        print(self.name + "'s speed: " + str(self.speed))

    def count_distance(self, other_position):
        return ((self.position[0] - other_position[0]) ** 2
                + (self.position[1] - other_position[1]) ** 2) ** 0.5

    def accelerate(self):
        acceleration = [0, 0]
        for planet in self.system.planets:
            if (planet != self) and (isinstance(planet, Planet) or isinstance(planet, Star)):
                distance = self.count_distance(planet.position)
                if distance < self.radius + planet.radius:
                    print("COLLISION!")
                    if self.mass > planet.mass:
                        self.system.collisions.append((self, planet))
                    else:
                        self.system.collisions.append((planet, self))
                else:
                    force = 6.6743 * 10**-8 * planet.mass / distance**2 * 1.296
                    for i in [0, 1]:
                        acceleration[i] += force * (
                                (planet.position[i] - self.position[i]) / distance)
        for i in [0, 1]:
            self.speed[i] += acceleration[i]
        return acceleration

    def eat_object(self, planet):
        print(planet.name + " fell at " + self.name + "!!!")
        for i in [0, 1]:
            self.speed[i] = (self.speed[i] * self.mass + planet.speed[i] * planet.mass)\
                            / (self.mass + planet.mass)
        self.mass += planet.mass
        self.radius = (self.radius ** 3 + planet.radius ** 3) ** (1 / 3)

    def warm_up(self):
        temperature = 0
        for planet in self.system.planets:
            if isinstance(planet, Star):
                distance = self.count_distance(planet.position)
                temperature += planet.light * 5646824.4 / distance**2
        return temperature


class Planet(Object):
    pass


class Star(Object):
    def __init__(self, system, name, mass, radius, position, speed, light,
                 turtles=None, color=None):
        super().__init__(system, name, mass, radius, position, speed, turtles, color)
        self.light = light

    def warm_up(self):
        return 0


class Spaceship(Object):
    def __init__(self, system, name, mass, radius, position, speed, program, fuel,
                 turtles=None, color=None):
        super().__init__(system, name, mass, radius, position, speed, turtles, color)
        self.program = program
        self.fuel = fuel

    def accelerate(self):
        super().accelerate()
        self.program(self, self.system)


class MassCenter(Object):
    def __init__(self, system, name, mass, radius, position, speed, objects,
                 turtles=None, color=None):
        super().__init__(system, name, mass, radius, position, speed, turtles, color)
        self.objects = objects
        self.move()

    def accelerate(self):
        return [0, 0]

    def warm_up(self):
        return 0

    def move(self):
        position = [0, 0]
        mass = 0
        for planet in self.objects:
            for i in [0, 1]:
                position[i] += planet.position[i] * planet.mass
            mass += planet.mass
        for i in [0, 1]:
            position[i] /= mass
        self.position = position
