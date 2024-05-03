import turtle

_turtle = turtle.Turtle()
_screen = turtle.Screen()
_screen.bgcolor("black")
_turtle.pencolor("yellow")

steps = 10
b = 90
_turtle.speed(3)
_turtle.pendown()
_turtle.goto(0, 0)
_turtle.showturtle()

i = 0

while i < 100: 
    _turtle.forward(steps)
    _turtle.right(b)
    steps += 5
    i += 1
    
turtle.done()