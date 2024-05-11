from algorithm import Algorithm

import random
import warnings
warnings.filterwarnings("ignore")

class PolicyIteration(Algorithm):
    
    def __init__(self, canvas, discount=0.9, iterations=500):
        Algorithm.__init__(self)
        self.canvas = canvas
        self.discount = discount
        self.iterations = iterations
        self.q_values = None
        self.policy = None
    
    
    def memoized_V(self, state):
        '''
        Retorna el valor calculado hasta el momento para el estado dado.
        '''
        i, j = state
        return self.q_values[i][j]
    
    
    def V(self, state, action):
        '''
        Calcula el nuevo valor para el estado 'state' si se ejecuta la acción 'action'.
        Para esto, se usa la ecuación de Bellman.
        '''
        t = 1 # El ruido es 0 dado que el canvas es deterministico. Entonces t = 1 siempre
        reward, state_prime = self.canvas.do_action(action)

        # Si estoy en un estado terminal y me muevo a un estado terminal, entonces
        # Jackspot! Esto lo hago para mostrarle a la tortuga que ya encontró el trazo
        # y que entonces debe seguir avanzando por el mismo. 
        if self.canvas.is_terminal(state) and self.canvas.is_terminal(state_prime):
            return 2000
        
        # En todos los otros casos, aplico la ecuación de Bellman para calcular los valores
        # que van a guiar a la tortuga a la primera casilla del trazo. 
        return t * (self.canvas.values_board[state[0]][state[1]] + self.discount * self.memoized_V(state_prime))
    

    
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
                        
    
    def policy_improvement(self):
        '''
        Éste método busca mejorar la política actual usando como insumo los q valores
        actuales.
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
                    self.policy[i][j] = best_action


    def policy_iteration(self):
        '''
        Éste método ejecuta el ciclo evaluación/mejora de la política a partir de
        un criterio de convergencia.
        '''

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
        
            # El primer paso de cada iteración es evaluar la política actual.
            self.policy_evaluation()

            # Una vez la política actual ha sido evaluada, entonces tratamos de mejorarla.
            self.policy_improvement()

        # Una vez terminado el ciclo evaluación/mejora, podemos actualizar el canvas
        # con los valores encontrados durante el algoritmo. Esto se hace simplemente
        # para poder visualizar los valores en el canvas.
        self.canvas.values_board = [[self.q_values[i][j] for j in range(self.canvas.ncols)] for i in range(self.canvas.nrows)]


    def run(self):
        '''
        Ejectuta el algoritmo. En este caso, lanza el algoritmo de 'policy_iteration'
        que encuentra la mejor política.
        '''
        self.policy_iteration()
