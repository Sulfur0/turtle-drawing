from canvas import Canvas
from policy_iteration import PolicyIteration
from value_iteration import ValueIteration
from logo import Logo

from utils import LoggerManager
logger = LoggerManager().getLogger()

class DrawingSinglePolicy():

    def __init__(self):
        self.rows, self.columns = 50, 50

        # Inicializo el tablero con todas las recompensas en cero
        self.rewards_board = [[' ' for _ in range(self.columns)] for _ in range(self.rows)]

        # Defino las recompensas de acuerdo a la figura que queremos dibujar.
        for i in range(self.rows):
            for j in range(self.columns):
                if i == 10 and j >= 10 and j <= 40:
                    self.rewards_board[i][j] = '+1'
                if i == 40 and j >= 10 and j <= 40:
                    self.rewards_board[i][j] = '+1'
                if j == 40 and i >= 10 and i <= 40:
                    self.rewards_board[i][j] = '+1'
                if j == 10 and i >= 10 and i <= 40:
                    self.rewards_board[i][j] = '+1'

        self.rewards_board[0][0] = 'S'
        self.canvas = Canvas(self.rewards_board)

    
    def train(self):
        '''
        Este método entrena el agente. Es decir, resuelve el MDP a partir del método
        de iteración de políticas a partir de las recompensas que se tienen en el canvas.

        Salidas:
        --------
        - canvas: El canvas que contiene el MDP que se quiere resolver
        - algorithm: El algorithm que soluciona el MDP. 
        '''

        logger.info('Inicio del entrenamiento. Calculando la política óptima a partir de las recompensas...')
        #algorithm = PolicyIteration(self.canvas)
        algorithm = ValueIteration(self.canvas)
        algorithm.run()
        logger.info('Fin del entrenamiento. Calculando la política óptima a partir de las recompensas...')
        return self.canvas, algorithm
    

    def draw(self, algorithm):
        '''
        Este método inicializa la tortuga y le entrega la política en la que se debe basar para dibujar.
        '''
        logger.info('La política está lista. Inicializo la tortuga para que empiece su dibujo')
        logo = Logo(canvas=algorithm.canvas, draw_rewards_only=True)
        logo.draw(algorithm, iterations=3000, collision_strategy='jump', ignore_terminals=False)
        logger.info('Dibujo terminado')


    def run(self):
        canvas, algorithm = self.train()
        self.draw(algorithm)