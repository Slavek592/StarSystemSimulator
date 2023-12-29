from turtle import RawTurtle, TurtleScreen
from tkinter import *
from math import sin, cos, atan, pi
import socket
from PIL import Image


class IWindow:
    def __init__(self, offset=None, scale=1, angle=0, spy_object=None,
                 angle_object=None):
        if offset is None:
            offset = [0, 0]
        self.turtles = []
        self.offset = offset
        self.scale = scale
        self.angle = angle
        self.spy_object = spy_object
        self.angle_object = angle_object

    def change_offset(self):
        if self.spy_object is not None:
            for turtle in self.turtles:
                turtle.temporary_offset = self.spy_object.position
        if self.angle_object is not None:
            if self.spy_object is not None:
                position = self.spy_object.position
            else:
                position = [0.0, 0.0]
            if position[0] - self.angle_object.position[0] == 0:
                if position[1] - self.angle_object.position[1] > 0:
                    angle = pi / 2
                else:
                    angle = -pi / 2
            else:
                angle = atan((position[1] - self.angle_object.position[1]) /
                             (position[0] - self.angle_object.position[0]))
            if position[0] - self.angle_object.position[0] < 0:
                angle = angle - pi
            for turtle in self.turtles:
                turtle.angle = angle + self.angle


class ITurtle:
    def __init__(self, offset=None, scale=1, angle=0):
        if offset is None:
            offset = [0, 0]
        self.offset = offset
        self.temporary_offset = [0.0, 0.0]
        self.angle = angle
        self.scale = scale

    def count_new_position(self, position):
        return (((position[0] - self.temporary_offset[0]) * cos(self.angle)
                 + (position[1] - self.temporary_offset[1]) * sin(self.angle)
                 - self.offset[0]) * self.scale,
                ((position[1] - self.temporary_offset[1]) * cos(self.angle)
                 - (position[0] - self.temporary_offset[0]) * sin(self.angle)
                 - self.offset[1]) * self.scale)


class MapWindow(Tk, IWindow):
    def __init__(self, title="Simulator", geometry="640x480",
                 offset=None, scale=1, angle=0, spy_object=None,
                 angle_object=None):
        IWindow.__init__(self, offset, scale, angle, spy_object, angle_object)
        Tk.__init__(self)
        self.running = True
        self.geometry(geometry)
        self.title(title)
        self.protocol("WM_DELETE_WINDOW", self.destroy_window)
        self.canvas = Canvas(self)
        self.canvas.pack(expand=True, fill=BOTH)
        self.screen = TurtleScreen(self.canvas)

    def screenshot(self, name="file"):
        self.canvas.postscript(file="Screenshots/" + name + ".eps")
        pic = Image.open("Screenshots/" + name + ".eps")
        pic.load()
        if pic.mode in ('P', '1'):
            pic = pic.convert("RGB")
        pic.save("Screenshots/" + name + ".png")

    def update_window(self):
        if self.running:
            self.update()

    def add_turtle(self):
        if self.spy_object is None:
            turtle = MapTurtle(self.screen, self.offset, self.scale, self.angle)
        else:
            turtle = MapTurtle(self.screen, [self.spy_object.position[0] + self.offset[0],
                               self.spy_object.position[1] + self.offset[1]], self.scale, self.angle)
        self.turtles.append(turtle)
        return turtle

    def destroy_window(self):
        self.running = False
        self.destroy()


class MapTurtle(ITurtle):
    def __init__(self, screen, offset=None, scale=1, angle=0):
        super().__init__(offset, scale, angle)
        self.turtle = RawTurtle(screen)
        self.turtle.shape("circle")
        self.turtle.shapesize(0.2, 0.2)
        self.turtle.speed(0)

    def go_to_position(self, position):
        self.turtle.goto(self.count_new_position(position))

    def prepare_turtle(self, position, color=None):
        if color is not None:
            self.turtle.color(color)
        self.turtle.penup()
        self.go_to_position(position)
        self.turtle.pendown()


class ExternalWindow(IWindow):
    def __init__(self, offset=None, scale=1, angle=0, spy_object=None,
                 angle_object=None):
        super().__init__(offset, scale, angle, spy_object, angle_object)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("0.0.0.0", 8000))
        self.socket.listen()
        connection, address = self.socket.accept()
        print(f"Connected by {address}")
        self.connection = connection

    def add_turtle(self):
        if self.spy_object is None:
            turtle = ExternalTurtle(len(self.turtles), self.connection, self.offset, self.scale, self.angle)
        else:
            turtle = ExternalTurtle(len(self.turtles), self.connection,
                                    [self.spy_object.position[0] + self.offset[0],
                                    self.spy_object.position[1] + self.offset[1]], self.scale, self.angle)
        self.turtles.append(turtle)
        return turtle


class ExternalTurtle(ITurtle):
    def __init__(self, name, connection, offset=None, scale=1, angle=0):
        super().__init__(offset, scale, angle)
        self.name = str(name)
        self.connection = connection

    def go_to_position(self, position, other_data=None):
        if other_data is not None:
            self.connection.sendall(
                bytes(self.name + ":" + str(self.count_new_position(position)) + ", "
                      + other_data + "<EOF>", "UTF-8"))
        else:
            self.connection.sendall(
                bytes(self.name + ":" + str(self.count_new_position(position)) + "<EOF>", "UTF-8"))

    def prepare_turtle(self, position, color=None):
        self.go_to_position(position, str(color))
