from algorithm import *

import warnings
warnings.filterwarnings("ignore")

from utils import LoggerManager
logger = LoggerManager().getLogger()

class ValueIteration(AlgorithmImpl):
    
    def __init__(self, canvas, discount=0.9, iterations=500, plot_policies=False):
        AlgorithmImpl.__init__(self, canvas, discount, iterations, plot_policies)
    

    def value_iteration(self):
        '''
        Éste método ejecuta el algoritmo de iteración de valores para calcular la política óptima del MDP. 
        En este caso, el MDP se compone del canvas y la tortuga.
        '''
        required_iterations = 0

        # Inicializamos los q valores arbitrariamente. Esta inicialización se decide
        # en el momento de inicializar las recompensas. Entonces, para la iteración
        # de políticas, simplemente hacemos una copia de los valores en el canvas.
        self.q_values = [[self.canvas.values_board[i][j] for j in range(self.canvas.ncols)] for i in range(self.canvas.nrows)]

        # Inicializamos la primera versión de la política (π) como una matriz vacía.
        # La política se construye durante el algoritmo de iteración de valores. 
        self.policy = [[None for j in range(self.canvas.ncols)] for i in range(self.canvas.nrows)]

        # Loop: Iteramos hasta la convergencia. En este caso, la convergencia se define
        #       en términos de la estabilidad de los q-valores de una iteración a otra. Si para
        #       una iteración i, los q-valores no cambian con respecto a la iteración i - 1, entonces
        #       decimos que los q-valores son estables y que se alcanzó la convergencia. 
        #       Para evitar ciclos infinitos en caso de no llegar a la convergencia, entonces se
        #       define un número máximo de iteraciones (self.iterations). 
        for _ in range(self.iterations):
            values_stable = True
            required_iterations += 1
            
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
                                    values_stable = False

                                best_action = action
                            self.canvas.state = state

                        # En este caso, construimos la política progresivamente al mismo tiempo que vamos
                        # calculando los q-valores. Una vez llegamos a la convergencia de los q-valores
                        # es decir, los q-valores no cambian de una iteración a otra, entonces sabemos
                        # que tenemos la política óptima.
                        self.policy[i][j] = best_action

            if values_stable : break

        # Una vez terminado el ciclo evaluación/mejora, podemos actualizar el canvas
        # con los valores encontrados durante el algoritmo. Esto se hace simplemente
        # para poder visualizar los valores en el canvas.
        self.canvas.values_board = [[self.q_values[i][j] for j in range(self.canvas.ncols)] for i in range(self.canvas.nrows)]
    
        return required_iterations
    

    def run(self):
        '''
        Ejectuta el algoritmo. En este caso, lanza el algoritmo de 'value_iteration' que encuentra la mejor política.
        '''
        logger.info('Ejecutando VALUE_ITERATION para resolver el MDP')
        required_iterations = self.value_iteration()
        logger.info(f'La ejecución de VALUE_ITERATION acaba de terminar. {required_iterations} fueron necesarias para alcanzar convergencia')