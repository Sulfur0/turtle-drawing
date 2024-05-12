from algorithm import *

import warnings
warnings.filterwarnings("ignore")

from utils import LoggerManager
logger = LoggerManager().getLogger()

class ValueIteration(AlgorithmImpl):
    
    def __init__(self, canvas, discount=0.9, iterations=500):
        AlgorithmImpl.__init__(self, canvas, discount, iterations)
    

    def value_iteration(self):
        '''
        Éste método ejecuta el algoritmo de iteración de valores para calcular la política óptima del MDP. 
        '''
        # Inicializamos los q valores arbitrariamente. Esta inicialización se decide
        # en el momento de inicializar las recompensas. Entonces, para la iteración
        # de políticas, simplemente hacemos una copia de los valores en el canvas.
        self.q_values = [[self.canvas.values_board[i][j] for j in range(self.canvas.ncols)] for i in range(self.canvas.nrows)]

        # Inicializamos la primera versión de la política (π) como una matriz vacía.
        # La política se construye durante el algoritmo de iteración de valores. 
        self.policy = [[None for j in range(self.canvas.ncols)] for i in range(self.canvas.nrows)]

        # Loop: Iteramos hasta la convergencia.
        for _ in range(self.iterations):
            
            # Loop: Tenemos que recorrer todos los estados. En este caso, los estados son
            #       las celdas de la matriz entonces entramos en un doble ciclo sobre los
            #       índices i y j. 
            for i in range(self.canvas.nrows):
                for j in range(self.canvas.ncols):
                    state = (i, j)

                    # Es importante excluir los estados que representan obstáculos. Esos
                    # estados no tienen ni recompensa ni valor. Entonces, no nos interesa
                    # iterar sobre ellos. 
                    if self.canvas.values_board[i][j] != None:
                        self.canvas.state = state

                        # Loop: Recorremos todas las acciones posibles a partir del estado
                        #       actual. Seleccionamos la que mejor q_valor nos da a partir
                        #       de los q_valores que hemos calculado hasta el momento.
                        best_action = self.policy[i][j]
                        best_value = self.q_values[i][j]
                        for action in self.canvas.get_possible_actions(state):
                            new_value = self.V(state, action)
                            self.canvas.do_action(action)
                            if new_value > best_value:
                                best_value = new_value

                                # No queremos modificar los q_valores sobre los estados terminales
                                # porque su valor inicial es la recompensa que guía el algoritmo.
                                if not self.canvas.is_terminal(state=(i, j)):
                                    self.q_values[i][j] = new_value
                                best_action = action
                            self.canvas.state = state

                        # En este caso, construimos la política progresivamente al mismo tiempo que vamos
                        # calculando los q-valores. Una vez llegamos a la convergencia de los q-valores
                        # es decir, los q-valores no cambian de una iteración a otra, entonces sabemos
                        # que tenemos la política óptima.
                        self.policy[i][j] = best_action
    

    def run(self):
        '''
        Ejectuta el algoritmo. En este caso, lanza el algoritmo de 'value_iteration' que encuentra la mejor política.
        '''
        logger.info('Ejecutando VALUE_ITERATION para resolver el MDP')
        self.value_iteration()