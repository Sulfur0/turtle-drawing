from canvas import Canvas
from policy import PolicyIteration
from logo import Logo

from utils import Logger
logger = Logger().get_logger()

class Drawing:

    def __init__(self):
        self.rows, self.columns = 50, 50

        # Inicializo el tablero con todas las recompensas en cero
        self.board = [[' ' for _ in range(self.columns)] for _ in range(self.rows)]

        # Defino las recompensas de acuerdo a la figura que queremos dibujar.
        for i in range(self.rows):
            for j in range(self.columns):
                if i == 10 and j >= 10 and j <= 40:
                    self.board[i][j] = '+1'
                if i == 40 and j >= 10 and j <= 40:
                    self.board[i][j] = '+1'
                if j == 40 and i >= 10 and i <= 40:
                    self.board[i][j] = '+1'
                if j == 10 and i >= 10 and i <= 40:
                    self.board[i][j] = '+1'

        self.board[0][0] = 'S'
        self.canvas = Canvas(self.board)

    
    def train(self):
        '''
        Este método entrena el agente. Es decir, resuelve el MDP a partir del método
        de iteración de políticas a partir de las recompensas que se tienen en el canvas.

        Salidas:
        --------
        - canvas: El canvas que contiene el MDP que se quiere resolver
        - agent: El agente que contiene la solución al MDP. 
        '''

        logger.info('Inicio del entrenamiento. Calculando la política óptima a partir de las recompensas...')
        agent = PolicyIteration(self.canvas)
        agent.policy_iteration()
        logger.info('Fin del entrenamiento. Calculando la política óptima a partir de las recompensas...')
        return self.canvas, agent
    

    def draw_policy(self, agent):
        '''
        Este método inicializa la tortuga y le entrega la política en la que se debe basar para dibujar.
        '''
        logger.info('La política está lista. Inicializo la tortuga para que empiece su dibujo')
        logo = Logo(canvas=agent.mdp)
        logo.draw(agent)
        logger.info('Dibujo terminado')


    def run(self):
        canvas, agent = self.train()
        self.draw_policy(agent)