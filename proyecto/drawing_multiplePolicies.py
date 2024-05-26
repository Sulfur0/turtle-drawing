from logo import Logo
from canvas import Canvas
from algorithm import Algorithm

from drawing_strategy import DrawingStrategy
from algorithm_policy_iteration import PolicyIteration
from algorithm_value_iteration import ValueIteration
from algorithm_monte_carlo import MonteCarlo
from algorithm_qlearning import QLearning
from rewards import Rewards, Size

from utils import LoggerManager
logger = LoggerManager().getLogger()

class DrawingMultiplePolicies(DrawingStrategy):

    def __init__(self, draw=True, algorithm_kind=Algorithm.POLICY_ITERATION):
        self.policies = []
        self.algorithm_kind = algorithm_kind

        # Inicializo la tortuga. En este caso, el ambiente aún no esta listo.
        if draw:
            self.logo = Logo(canvas=None)
    

    def train(self, canvas, episodes=10):
        '''
        Este método entrena el agente. Es decir, resuelve el MDP a partir del método
        de iteración de políticas a partir de las recompensas que se tienen en el canvas.
        Entradas:
        --------
        - canvas: El canvas que contiene el MDP que se quiere resolver.
        '''

        logger.info('Inicio del entrenamiento. Calculando la política óptima a partir de las recompensas...')
        
        if self.algorithm_kind == Algorithm.VALUE_ITERATION:
            algorithm = ValueIteration(canvas)
        if self.algorithm_kind == Algorithm.POLICY_ITERATION:
            algorithm = PolicyIteration(canvas)
        if self.algorithm_kind == Algorithm.MONTE_CARLO:
            algorithm = MonteCarlo(canvas, episodes=episodes)
        if self.algorithm_kind == Algorithm.Q_LEARNING:
            algorithm = QLearning(canvas, episodes=episodes)
        
        algorithm.run()
        logger.info('Fin del entrenamiento. Calculando la política óptima a partir de las recompensas...')
        return algorithm


    def draw(self, solutions):
        '''
        Este método inicializa la tortuga y le entrega la solución en la que se debe basar para dibujar.
        '''
        
        iteration = 0
        for solution in solutions:
            logger.info('La política para el siguiente trazo está lista. Le pido a la tortuga que empiece su dibujo')
            self.logo.canvas = solution[0]

            # La primera iteración consiste en buscar el primer vértice de la figura. Como no quiero dibujar esa
            # búsqueda, entonces levanto el lápiz para esa primera iteración. 
            if iteration == 0:
                self.logo._turtle.penup()
            else:
                self.logo._turtle.pendown()
                
            self.logo.draw(solution[1], state=solution[2])
            logger.info('Trazo terminado.')
            iteration += 1

        self.logo.done()


    def create_canvases(self, rewards_boards, plot=False):
        """
        Crea la lista de canvas para cada iteración del dibujo. Se debe crear un canvas por cada
        vértice de la figura tomando en cuenta el punto anterior como inicio del siguiente.
        No se establece la recompensa inicial en la instanciacion de la clase sino en este punto.
        Se retorna una lista de políticas, una por cada trazo que la tortuga debe dibujar. 
        """
        solutions = []
        
        for rewards_board in rewards_boards:
            canvas = Canvas(rewards_board)
            algorithm = self.train(canvas)
            solutions += [(canvas, algorithm, canvas.initial_state),]
            # En este punto ya se han actualizado las politicas, aqui se debe dibujar hasta el destino.
            if plot:
                canvas.plot_rainbow()
                canvas.plot_policy(algorithm.policy)
                ##if self.algorithm_kind == Algorithm.Q_LEARNING:
                ##    actions, values = algorithm.actions_values()
                ##    algorithm.canvas.plot_action(actions, values)
                ##else:
                ##    canvas.plot_rainbow()
                ##    canvas.plot_policy(algorithm.policy)

        logger.info("Terminar")

        return solutions


    def run(self):
        rewards_boards = Rewards().square(size=Size.M)
        solutions = self.create_canvases(rewards_boards)
        self.draw(solutions)