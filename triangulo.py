import turtle

t = turtle.Turtle()
s = turtle.Screen()
print(s.window_width(), "x", s.window_height())


s.bgcolor("black")
t.pencolor("yellow")

t.speed(1)
t.penup()
t.goto(-100, -100)  # Mueve la tortuga a la posición inicial
t.pendown()
t.showturtle()

# Dibujando el triángulo equilátero
t.begin_fill()  # Comienza a llenar el triángulo con el color
t.goto(100, -100)
t.goto(0, 100)
t.goto(-100, -100)

turtle.done()   # Mantiene la ventana abierta hasta que se cierre manualmente