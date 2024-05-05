import turtle
import random

class Logo:

    def __init__(self, env, step_size=2):
        self.env = env
        self.step_size = step_size
        self._turtle = turtle.Turtle()
        self._screen = turtle.Screen()
        self._turtle.speed(3)
        self._turtle.penup()
        self.go_to(self.env.state)
        self._turtle.left(90)


    def logo_coordinates(self, position):
        i, j = position
        x = j * self.step_size
        y = i * self.step_size * -1
        return x, y
    

    def down(self):
        '''
        Mueve la torguga hacia abajo tantas unidades en self.step_size
        Si la posición de llegada de este movimiento tiene una recompensa,
        entonces la tortuga baja el lápiz para dibujar.
        '''
        self.prepare_pen()
        self._turtle.right(180)
        self._turtle.forward(self.step_size)
        self._turtle.left(180)
        self._turtle.penup()


    def up(self):
        '''
        Mueve la torguga hacia arriba tantas unidades en self.step_size
        Si la posición de llegada de este movimiento tiene una recompensa,
        entonces la tortuga baja el lápiz para dibujar.
        '''
        self.prepare_pen()
        self._turtle.forward(self.step_size)
        self._turtle.penup()
        

    def left(self):
        '''
        Mueve la torguga hacia la izquierda tantas unidades en self.step_size
        Si la posición de llegada de este movimiento tiene una recompensa,
        entonces la tortuga baja el lápiz para dibujar.
        '''
        self.prepare_pen()
        self._turtle.left(90)
        self._turtle.forward(self.step_size)
        self._turtle.right(90)
        self._turtle.penup()
        

    def right(self):
        '''
        Mueve la torguga hacia la derecha tantas unidades en self.step_size
        Si la posición de llegada de este movimiento tiene una recompensa,
        entonces la tortuga baja el lápiz para dibujar.
        '''
        self.prepare_pen()
        self._turtle.right(90)
        self._turtle.forward(self.step_size)
        self._turtle.left(90)
        self._turtle.penup()
        


    def go_to(self, position):
        logo_target = self.logo_coordinates(position)
        self._turtle.goto(logo_target[0], logo_target[1])
        print(f'OK, jumping to {logo_target}')


    def prepare_pen(self):
        if self.env.is_terminal(state=self.env.state):
            self._turtle.pendown()
            print(f'I am rewarded in this position {self.logo_coordinates(self.env.state)}!. Drawing')
        else:
            print(f'I am not rewarded in this position {self.logo_coordinates(self.env.state)}!. I won''t draw')

    
    def draw(self, agent, iterations=300):

        state = (0, 0)
        agent.mdp.initial_state = state
        agent.mdp.state = state
        pivot_state = state
        
        last_action = None
        for _ in range(iterations):
            policy = agent.policy[pivot_state[0]][pivot_state[1]]

            if agent.mdp.actions_collide(policy, last_action):
                pivot_state = (random.randrange(0, self.env.nrows), random.randrange(0, self.env.ncols))
                self.go_to(pivot_state)
                agent.mdp.state = pivot_state
                print('Collision. Jumping')
                last_action = None

            else:
                if policy == 'down':
                    self.down()
                if policy == 'up':
                    self.up()
                if policy == 'left':
                    self.left()
                if policy == 'right':
                    self.right()

                last_action = policy
                agent.mdp.do_action(policy)
                pivot_state = agent.mdp.state

            print(f'current position: pivot_state: {pivot_state}, mdp.state: {agent.mdp.state} run {policy}')