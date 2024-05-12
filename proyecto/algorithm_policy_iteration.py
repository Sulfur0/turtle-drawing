from algorithm import *

import random
import warnings
warnings.filterwarnings("ignore")

from utils import LoggerManager
logger = LoggerManager().getLogger()

class PolicyIteration(AlgorithmImpl):
    
    def __init__(self, canvas, discount=0.9, iterations=20, plot_policies=False):
        AlgorithmImpl.__init__(self, canvas, discount, iterations, plot_policies)

    
    def policy_evaluation(self):
        '''
        Este método evalúa la política actual usando la ecuación de Bellman sobre los
        valores V calculados hasta el momento. 
        La política actual es la que tenemos en el attibute self.policy del objeto.
        '''

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

                    # Tampoco queremos calcular los valores sobre los estados terminales
                    # porque su valor inicial es la recompensa que guía el algoritmo.
                    if not self.canvas.is_terminal():
                        # Calculo la ecuación de Bellman para cada uno de los estados a los que puedo llegar
                        # con las acciones válidas desde el estado actual. 
                        action = self.policy[i][j]
                        self.q_values[i][j] = self.V(state, action)
                        self.canvas.state = state     

        if self.plot_policies:
            self.canvas.plot_policy(self.policy)              
                        
    
    def policy_improvement(self):
        '''
        Éste método busca mejorar la política actual usando como insumo los q valores
        actuales.

        Salidas:
        ------------
        - policy_stable: True si no hay mejora con respecto a la última iteración. False de lo contrario.

        '''
        policy_stable = True
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
                    
                    if self.policy[i][j] != best_action:
                        policy_stable = False
                        self.policy[i][j] = best_action
        
        return policy_stable


    def policy_iteration(self):
        '''
        Éste método ejecuta el ciclo evaluación/mejora de la política a partir de
        un criterio de convergencia.

        Salidas:
        ------------
        - required_iterations: Cantidad de iteraciones requeridas para lograr convergencia en la política.
        '''
        required_iterations = 0

        # Inicializamos los q valores arbitrariamente. Esta inicialización se decide
        # en el momento de inicializar las recompensas. Entonces, para la iteración
        # de políticas, simplemente hacemos una copia de los valores en el canvas.
        self.q_values = [[self.canvas.values_board[i][j] for j in range(self.canvas.ncols)] for i in range(self.canvas.nrows)]

        # Inicializamos la primera versión de la política (π) aleatoriamente. Naturalmente, 
        # no va a ser la política óptima pero será la política que empezaremos a 
        # optimizar. El objetivo es hallar la política óptima (π*) como resultado de
        # este algoritmo.
        self.policy = [[random.choice(self.canvas.get_possible_actions((i, j))) if self.canvas.values_board[i][j] != None else None for j in range(self.canvas.ncols)] for i in range(self.canvas.nrows)]

        # Loop: Iniciamos el ciclo de optimización. En este caso, usamos una cantidad
        # fija de iteraciones (self.iterations) pero podemos también utilizar un criterio 
        # de convergencia.
        for _ in range(self.iterations):
            required_iterations += 1
        
            # El primer paso de cada iteración es evaluar la política actual.
            self.policy_evaluation()

            # Una vez la política actual ha sido evaluada, entonces tratamos de mejorarla.
            convergence = self.policy_improvement()

            if convergence : break

        # Una vez terminado el ciclo evaluación/mejora, podemos actualizar el canvas
        # con los valores encontrados durante el algoritmo. Esto se hace simplemente
        # para poder visualizar los valores en el canvas.
        self.canvas.values_board = [[self.q_values[i][j] for j in range(self.canvas.ncols)] for i in range(self.canvas.nrows)]
    
        return required_iterations


    def run(self):
        '''
        Ejectuta el algoritmo. En este caso, lanza el algoritmo de 'policy_iteration'
        que encuentra la mejor política.
        '''
        logger.info('Ejecutando POLICY_ITERATION para resolver el MDP')
        required_iterations = self.policy_iteration()
        logger.info(f'La ejecución de POLICY_ITERATION acaba de terminar. {required_iterations} fueron necesarias para alcanzar convergencia')
