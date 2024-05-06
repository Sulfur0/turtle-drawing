from canvas import Canvas
from policy import PolicyIteration
from logo import Logo

from utils import LoggerManager
logger = LoggerManager().getLogger()

class Drawing:

    def __init__(self, figure_sequence, dimensions):
        
        self.figure_sequence = figure_sequence        

        self.rows, self.columns = dimensions

        # Inicializo el tablero con todas las recompensas en cero
        self.rewards_board = [[' ' for _ in range(self.columns)] for _ in range(self.rows)]   
        self.starting_point = (0, 0)
        si, sj = self.starting_point
        self.rewards_board[si][sj] = 'S'
        self.canvas = None
        self.policies = []

    
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

    def create_canvases(self):
        """
        crea la lista de canvas para cada iteracion del dibujo
        se debe crear un canvas por vertice de la figura tomando en cuenta el punto anterior como 
        inicio del siguiente
        no se establece la recompensa inicial en la instanciacion de la clase sino en este punto        
        """
        print("rewards_board: ",len(self.rewards_board))
        for iter_num in range(len(self.figure_sequence)):
            iteration = self.figure_sequence[iter_num]
            i,j = iteration
            self.rewards_board[int(i/5)][int(j/5)] = '+1'
            self.canvas = Canvas(self.rewards_board)
            canvas, agent = self.train()
            # En este punto ya se han actualizado las politicas, aqui se debe dibujar hasta el destino.
            canvas.plot_policy(agent.policy)
            # establecemos el inicio para la siguiente iteracion
            si, sj = self.starting_point
            self.rewards_board[si][sj] = ' '
            self.starting_point = (int(i/5) , int(j/5))
            self.rewards_board[int(i/5)][int(j/5)] = 'S'
            
            if(iter_num == len(self.figure_sequence)-1):
                print("terminar")

    def run(self):
        self.create_canvases()
        # canvas, agent = self.train()
        # print(canvas)

        # self.draw_policy(agent)