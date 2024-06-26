from logo import Logo
from canvas import Canvas
from algorithm import Algorithm

from drawing_strategy import DrawingStrategy

from utils import LoggerManager
logger = LoggerManager().getLogger()

from algorithm_policy_iteration import PolicyIteration
from algorithm_value_iteration import ValueIteration
from algorithm_monte_carlo import MonteCarlo
from algorithm_qlearning import QLearning

class DrawingSinglePolicy(DrawingStrategy):


    def __init__(self, algorithm_kind=Algorithm.POLICY_ITERATION):
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
        self.algorithm_kind = algorithm_kind
    

    def train(self, canvas, episodes=1000, plot_policies=False):
        '''
        Este método entrena el agente. Es decir, resuelve el MDP a partir del método
        de iteración de políticas a partir de las recompensas que se tienen en el canvas.
        Salidas:
        --------
        - canvas: El canvas que contiene el MDP que se quiere resolver
        - algorithm: El algorithm que soluciona el MDP. 
        '''

        logger.info('Inicio del entrenamiento. Calculando la política óptima a partir de las recompensas...')
        algorithm = None

        if self.algorithm_kind == Algorithm.VALUE_ITERATION:
            algorithm = ValueIteration(canvas, plot_policies=plot_policies)
        if self.algorithm_kind == Algorithm.POLICY_ITERATION:
            algorithm = PolicyIteration(canvas, plot_policies=plot_policies)
        if self.algorithm_kind == Algorithm.MONTE_CARLO:
            algorithm = MonteCarlo(canvas, episodes=episodes, plot_policies=plot_policies)
        if self.algorithm_kind == Algorithm.Q_LEARNING:
            algorithm = QLearning(canvas, episodes=episodes, plot_policies=plot_policies)
        
        algorithm.run()
        logger.info('Fin del entrenamiento. Calculando la política óptima a partir de las recompensas...')
        return algorithm


    def draw(self, algorithm):
        '''
        Este método inicializa la tortuga y le entrega la política en la que se debe basar para dibujar.
        '''
        logger.info('La política está lista. Inicializo la tortuga para que empiece su dibujo')
        logo = Logo(canvas=algorithm.canvas, draw_rewards_only=True)
        logo.draw(algorithm, iterations=3000, collision_strategy='jump', ignore_terminals=False)
        logger.info('Dibujo terminado')


    def run(self):
        canvas = Canvas(self.rewards_board)
        algorithm = self.train(canvas)
        self.draw(algorithm)