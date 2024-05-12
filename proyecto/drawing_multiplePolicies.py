from canvas import Canvas
from policy_iteration import PolicyIteration
from logo import Logo

from utils import LoggerManager
logger = LoggerManager().getLogger()

class DrawingMultiplePolicies():

    def __init__(self, figure_sequence, dimensions, draw=True):
        self.figure_sequence = figure_sequence        
        self.rows, self.columns = dimensions

        # Inicializo el tablero con todas las recompensas en cero
        self.rewards_board = [[' ' for _ in range(self.columns)] for _ in range(self.rows)]   
        self.starting_point = (0, 0)
        si, sj = self.starting_point
        self.rewards_board[si][sj] = 'S'
        self.policies = []

        # Inicializo la tortuga. En este caso, el ambiente aún no esta listo.
        if draw:
            self.logo = Logo(canvas=None)

    
    def train(self, canvas):
        '''
        Este método entrena el agente. Es decir, resuelve el MDP a partir del método
        de iteración de políticas a partir de las recompensas que se tienen en el canvas.

        Salidas:
        --------
        - canvas: El canvas que contiene el MDP que se quiere resolver
        '''

        logger.info('Inicio del entrenamiento. Calculando la política óptima a partir de las recompensas...')
        algorithm = PolicyIteration(canvas)
        algorithm.run()
        logger.info('Fin del entrenamiento. Calculando la política óptima a partir de las recompensas...')
        return canvas, algorithm
    

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


    def create_canvases(self, plot=False):
        """
        Crea la lista de canvas para cada iteración del dibujo. Se debe crear un canvas por cada
        vértice de la figura tomando en cuenta el punto anterior como inicio del siguiente.
        No se establece la recompensa inicial en la instanciacion de la clase sino en este punto.
        Se retorna una lista de políticas, una por cada trazo que la tortuga debe dibujar. 
        """
        print("rewards_board: ",len(self.rewards_board))
        solutions = []
        for iter_num in range(len(self.figure_sequence)):
            iteration = self.figure_sequence[iter_num]
            i,j = iteration
            self.rewards_board[int(i/5)][int(j/5)] = '+1'
            canvas = Canvas(self.rewards_board)
            canvas, algorithm = self.train()
            solutions += [(canvas, algorithm, self.starting_point),]
            # En este punto ya se han actualizado las politicas, aqui se debe dibujar hasta el destino.
            if plot:
                canvas.plot_policy(algorithm.policy)

            # establecemos el inicio para la siguiente iteracion
            si, sj = self.starting_point
            self.rewards_board[si][sj] = ' '
            self.starting_point = (int(i/5) , int(j/5))
            self.rewards_board[int(i/5)][int(j/5)] = 'S'
            
            if(iter_num == len(self.figure_sequence)-1):
                print("terminar")

        return solutions


    def run(self):
        solutions = self.create_canvases()
        self.draw(solutions)