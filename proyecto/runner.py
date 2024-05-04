from canvas import Canvas
from policy import PolicyIteration

rows, columns = 50, 50

# Inicializo el tablero con todas las recompensas en cero
board = [[' ' for _ in range(columns)] for _ in range(rows)]

# Defino las recompensas de acuerdo a la figura que queremos dibujar.
for i in range(rows):
    for j in range(columns):
        if i == 10 and j >= 10 and j <= 40:
            board[i][j] = '+1'
        if i == 40 and j >= 10 and j <= 40:
            board[i][j] = '+1'
        if j == 40 and i >= 10 and i <= 40:
            board[i][j] = '+1'
        if j == 10 and i >= 10 and i <= 40:
            board[i][j] = '+1'

board[0][0] = 'S'
env = Canvas(board)

# Creación del agente
agent = PolicyIteration(env)
agent.policy_iteration()

iterations = 1000
state = (0, 0)
agent.mdp.initial_state = state
agent.mdp.state = state
pivot_state = state
steps = 1

import turtle

_turtle = turtle.Turtle()
_screen = turtle.Screen()
_turtle.speed(100)
_turtle.pendown()
_turtle.goto(0, 0)
_screen.bgcolor("black")
_turtle.pencolor("yellow")
_turtle.left(90)

def run_down():
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

last_action = None

import random

for iteration in range(iterations):
    policy = agent.policy[pivot_state[0]][pivot_state[1]]

    # If the actions collide, then disobey
    if agent.mdp.actions_collide(policy, last_action):
        #policy = agent.mdp.get_opposite(policy)
        policy = random.choice(agent.mdp.get_possible_actions(pivot_state))

    print(f'from {pivot_state} run {policy}')
    if policy == 'down':
        run_down()
    if policy == 'up':
        run_up()
    if policy == 'left':
        run_left()
    if policy == 'right':
        run_right()

    last_action = policy
    agent.mdp.do_action(policy)
    pivot_state = agent.mdp.state



turtle.done()