import turtle

_turtle = turtle.Turtle()
_screen = turtle.Screen()
_screen.bgcolor("black")
_turtle.pencolor("yellow")

steps = 10
b = 90
_turtle.speed(3)
_turtle.pendown()
_turtle.showturtle()


#_turtle.goto(50, -50)


#def logo_coordinates(i, j):
#    x = j
#    y = -i
#    return x, y

def logo_coordinates(i, j):
        #i, j = position
        x = j
        y = i * -1
        return x, y


_turtle.goto(logo_coordinates(23, 46))
#_turtle.goto(logo_coordinates(0, 50))
#_turtle.goto(logo_coordinates(50, 50))

#i = 0

#while i < 100: 
#    _turtle.forward(steps)
#    _turtle.right(b)
#    steps += 5
#    i += 1
    
turtle.done()