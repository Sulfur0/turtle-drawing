import turtle

_turtle = turtle.Turtle()
_screen = turtle.Screen()
_screen.bgcolor("black")
_turtle.pencolor("yellow")

steps = 100
_turtle.speed(3)
_turtle.penup()
_turtle.goto(-150, -50)
_turtle.showturtle()
_turtle.pendown()


_turtle.forward(steps)
_turtle.right(60)
_turtle.forward(steps)
_turtle.left(120)
_turtle.forward(steps)

_turtle.right(60)
_turtle.forward(steps)
_turtle.left(120)
_turtle.forward(steps)

_turtle.right(60)
_turtle.forward(steps)
_turtle.left(120)
_turtle.forward(steps)

_turtle.right(60)
_turtle.forward(steps)
_turtle.left(120)
_turtle.forward(steps)
_turtle.right(60)

_turtle.forward(steps)
_turtle.left(120)
_turtle.forward(steps)
_turtle.right(60)
_turtle.forward(steps)

    
turtle.done()