import math
from turtle import RawTurtle, TurtleScreen
from tkinter import *
from math import sin, cos, atan, pi


class MapWindow(Tk):
    def __init__(self, title="Simulator", geometry="640x480",
                 offset=[0, 0], scale=1, angle=0, spy_object=None,
                 angle_object=None):
        super().__init__()
        self.running = True
        self.geometry(geometry)
        self.title(title)
        self.protocol("WM_DELETE_WINDOW", self.destroy_window)
        self.canvas = Canvas(self)
        self.canvas.pack(expand=True, fill=BOTH)
        self.turtles = []
        self.screen = TurtleScreen(self.canvas)
        self.offset = offset
        self.scale = scale
        self.angle = angle
        self.spy_object = spy_object
        self.angle_object = angle_object

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

    def destroy_window(self):
        self.running = False
        self.destroy()


class MapTurtle:
    def __init__(self, screen, offset=[0, 0], scale=1, angle=0):
        self.turtle = RawTurtle(screen)
        self.turtle.shape("circle")
        self.turtle.shapesize(0.2, 0.2)
        self.turtle.speed(0)
        self.offset = offset
        self.temporary_offset = [0.0, 0.0]
        self.angle = angle
        self.scale = scale

    def go_to_position(self, position):
        self.turtle.goto(((position[0] - self.temporary_offset[0]) * cos(self.angle)
                          + (position[1] - self.temporary_offset[1]) * sin(self.angle)
                          - self.offset[0]) * self.scale,
                         ((position[1] - self.temporary_offset[1]) * cos(self.angle)
                          - (position[0] - self.temporary_offset[0]) * sin(self.angle)
                          - self.offset[1]) * self.scale)

    def prepare_turtle(self, position, color=None):
        if color is not None:
            self.turtle.color(color)
        self.turtle.penup()
        self.go_to_position(position)
        self.turtle.pendown()
