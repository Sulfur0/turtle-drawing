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
_turtle.left(90)

def run_down():
    print('down')
    _turtle.right(180)
    _turtle.forward(steps)
    _turtle.left(180)

def run_up():
    _turtle.forward(steps)

def run_left():
    _turtle.left(90)
    _turtle.forward(steps)
    _turtle.right(90)

def run_right():
    _turtle.right(90)
    _turtle.forward(steps)
    _turtle.left(90)

run_right()

run_up()
run_up()
run_up()
run_up()
run_up()
run_up()
run_up()
run_up()
run_up()

run_down()
run_down()
run_down()
run_down()
    
turtle.done()