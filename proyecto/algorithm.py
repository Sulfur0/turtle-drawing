class AlgorithmImpl:

    def __init__(self, canvas, discount=0.9, iterations=500, plot_policies=False):
        self.canvas = canvas
        self.discount = discount
        self.iterations = iterations
        self.plot_policies
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

    def run(self):
        pass


from enum import Enum

class Algorithm(Enum):
    VALUE_ITERATION = 1
    POLICY_ITERATION = 2
    MONTE_CARLO = 3
    TEMPORAL_DIFFERENCE = 4