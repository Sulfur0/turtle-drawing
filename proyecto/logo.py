import turtle
import random

from utils import LoggerManager
logger = LoggerManager().getLogger()

import warnings
warnings.filterwarnings("ignore")

class Logo:

    def __init__(self, canvas, step_size=7, draw_rewards_only=False):

        # Configuración de la tortuga y de la pantalla
        self._turtle = turtle.Turtle()
        self._turtle.penup()
        self._turtle.speed(30)
        self._turtle.left(90)
        self._turtle.pencolor("yellow")
        self._screen = turtle.Screen()
        self._screen.bgcolor("black")

        # Inicialización del estado inicial del agente.
        self.canvas = canvas
        self.step_size = step_size
        if self.canvas != None:
            self.go_to(self.canvas.initial_state)
        self.draw_rewards_only=draw_rewards_only


    def logo_coordinates(self, position):
        '''
        El sistema de coordenadas de la tortuga no es el mismo que el sistema de
        coordenadas del canvas. Mientras que la tortuga se mueve sobre un sistema
        cartesiano donde el origen está en el punto inferior izquerdo, el canvas
        inicia en el punto superior izquerdo. 
        
        Esto es porque el canvas esta representado
        como una matriz de python, la primera fila es la fila superior mientras que
        la primera columna es la de más a la izquirda. 
        
        Además, el canvas representa estados mientras que la posición de la tortuga
        debe tener en cuenta la distancia entre los estados que está definida por el 
        tamaño del paso. 

        Este método se encarga de hacer la transformación. Recibe como parámetro una
        coordenada en el sistema matricial (del canvas) y retorna la coordenada 
        correspondiente en el sistema cartesiado (usado por logo).
        '''
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
        if self.draw_rewards_only:
            self._turtle.penup()


    def up(self):
        '''
        Mueve la torguga hacia arriba tantas unidades en self.step_size
        Si la posición de llegada de este movimiento tiene una recompensa,
        entonces la tortuga baja el lápiz para dibujar.
        '''
        self.prepare_pen()
        self._turtle.forward(self.step_size)
        if self.draw_rewards_only:
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
        if self.draw_rewards_only:
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
        if self.draw_rewards_only:
            self._turtle.penup()
        

    def go_to(self, position, draw=False):
        '''
        Este método hace que la tortuga salte hacia una posición diferente de la actual.
        El salto puede dejar trazo o no dependiendo del valor del parámetro 'draw'.
        '''
        logo_target = self.logo_coordinates(position)
        if draw:
            self._turtle.pendown()
        self._turtle.goto(logo_target[0], logo_target[1])
        self._turtle.penup()
        logger.info(f'OK, jumping to {logo_target}')

    
    def prepare_pen(self):
        '''
        Este método prepara el lápiz para el movimiento de acuerdo con las recompensas. 
        Si existe una recompensa en el estado actual del ambiente, entonces se baja el lápiz
        para dibujar. De lo contrario, el lápiz se deja levantado para no hacer trazos sobre
        estados que no tienen recompensa porque no son parte del dibujo.
        '''
        if self.draw_rewards_only :
            if self.canvas.is_terminal(state=self.canvas.state):
                self._turtle.pendown()
    

    def draw(self, agent, iterations=15, state=(0, 0), collision_strategy='stop', ignore_terminals=True):
        '''
        Este método usa la política en el agente para dibujar. El algoritmo de dibujo se basa en iteraciones, 
        cada iteración da un paso desde el estado actual en la dirección dictada por la política. 
        En algunos casos hay colisiones y es necesario desobedecer la política y saltar a otro lugar del tablero para 
        evitar ciclos infinitos. 

        Entradas:
        -----------

        - collision_strategy: Estrategia que se debe seguir en caso de colisiones. Dos opciones son posibles:
        'stop' que detiene la ejecución saliendo del ciclo de dibujo y del método, y 'jump' que hace que la tortuga
        salte a un punto aleatorio del tablero. 

        - ignore_terminals: Ignora el movimiento dictado por la política en un estado terminal. Esos movimientos
        no nos interesan cuando estamos calculando un trazo porque el estado terminal no debe cambiar dado que es el
        estado inicial de la siguiente iteración.
        '''
        agent.canvas.initial_state = state
        agent.canvas.state = state
        pivot_state = state
        logger.info(f'Inicio un trazo en el estado: {state}')
        
        last_action = None
        for _ in range(iterations):

            if ignore_terminals and self.canvas.is_terminal(state=self.canvas.state):
                return

            policy = agent.policy[pivot_state[0]][pivot_state[1]]
            logger.info(f'La política me dice que debo ir: {policy}')

            # Una colisión se da cuando la política en el estado de llegada de un movimiento le pide
            # a la tortuga volver a la posición en la que se encuentra actualmente. Esto es una colisión
            # porque se crea un ciclo infinito. 
            if agent.canvas.actions_collide(policy, last_action):

                # En este caso, la estrategia es 'jump', entonces le pedimos a la tortuga que sale a un estado
                # aleatorio diferente del tablero para abordar el dibujo por otro camino. 
                if collision_strategy == 'jump':
                    pivot_state = (random.randrange(0, self.canvas.nrows), random.randrange(0, self.canvas.ncols))
                    self.go_to(pivot_state)
                    agent.canvas.state = pivot_state
                    logger.info(f'Collision! Jumping to a random state: {pivot_state}')
                    last_action = None

                # En caso, la estrategia es 'stop' y entonces detenemos el dibujo y salimos del método.
                else:
                    return
            
            # Cuando no hay colisión, entonces la tortuga se mueve en la dirección que dicta la política en
            # en el estado actual.
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
                agent.canvas.do_action(policy)
                pivot_state = agent.canvas.state
                logger.info(f'Mi nuevo estado luego de la acción es: {pivot_state}')


    def done(self):
        turtle.done()