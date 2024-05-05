import turtle

_turtle = turtle.Turtle()
_screen = turtle.Screen()
_screen.bgcolor("black")
_turtle.pencolor("yellow")

steps = 100
angle = 60
_turtle.speed(3)
_turtle.penup()
_turtle.goto(-50, -50)
_turtle.showturtle()
_turtle.pendown()


_turtle.forward(steps)
_turtle.left(angle)

_turtle.forward(steps)
_turtle.left(angle)

_turtle.forward(steps)
_turtle.left(angle)

_turtle.forward(steps)
_turtle.left(angle)

_turtle.forward(steps)
_turtle.left(angle)

_turtle.forward(steps)
_turtle.left(angle)

    
turtle.done()