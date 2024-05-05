from canvas import Canvas
from policy import PolicyIteration
from logo import Logo
import random

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

iterations = 30
state = (0, 0)
agent.mdp.initial_state = state
agent.mdp.state = state
pivot_state = state

logo = Logo()
last_action = None

for iteration in range(iterations):
    policy = agent.policy[pivot_state[0]][pivot_state[1]]

    if agent.mdp.actions_collide(policy, last_action):
        pivot_state = (random.randrange(rows), random.randrange(columns))
        logo.go_to(pivot_state)
        agent.mdp.state = pivot_state
        print('Collision. Jumping')
        last_action = None

    else:
        if policy == 'down':
            logo.down()
        if policy == 'up':
            logo.up()
        if policy == 'left':
            logo.left()
        if policy == 'right':
            logo.right()

        last_action = policy
        agent.mdp.do_action(policy)
        pivot_state = agent.mdp.state

    print(f'current position: pivot_state: {pivot_state}, mdp.state: {agent.mdp.state} run {policy}')

