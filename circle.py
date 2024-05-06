import turtle

t = turtle.Turtle()
s = turtle.Screen()
s.bgcolor("black")
t.pencolor("yellow")

a = 0
b = 0
t.speed(1)
t.penup()
t.goto(0, -100)
t.pendown()
t.showturtle()

# Dibujando el círculo
t.begin_fill()  # Comienza a llenar el círculo con el color
t.circle(100)   # Dibuja un círculo de radio 100
t.end_fill()    # Termina de llenar el círculo

turtle.done()   # Mantiene la ventana abierta hasta que se cierre manualmente