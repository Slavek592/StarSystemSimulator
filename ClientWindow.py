import socket
from turtle import Turtle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((input("Print the IP address of the host (for example \"127.0.0.1\")\n"), 8000))
turtles = []
remaining = ""
adding_turtles = True
while adding_turtles:
    data = (remaining + str(s.recv(1024))[2:-1]).split("<EOF>")
    for message_number in range(len(data)-1):
        message = data[message_number]
        number, positions = message.split(":")
        if int(number) == len(turtles):
            new_turtle = Turtle()
            new_turtle.shape("circle")
            new_turtle.shapesize(0.2, 0.2)
            new_turtle.speed(0)
            x, y, color = positions.replace("(", "").replace(")", "").split(", ")
            if color != "None":
                new_turtle.color(color)
            new_turtle.penup()
            new_turtle.goto(float(x), float(y))
            new_turtle.pendown()
            turtles.append(new_turtle)
        else:
            adding_turtles = False
            x, y = positions.replace("(", "").replace(")", "").split(", ")
            turtles[int(number)].goto(float(x), float(y))
    remaining = data[-1]
while True:
    data = (remaining + str(s.recv(1024))[2:-1]).split("<EOF>")
    for message_number in range(len(data)-1):
        message = data[message_number]
        number, positions = message.split(":")
        x, y = positions.replace("(", "").replace(")", "").split(", ")
        turtles[int(number)].goto(float(x), float(y))
    remaining = data[-1]
