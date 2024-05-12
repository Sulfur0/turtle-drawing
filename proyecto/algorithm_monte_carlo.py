from algorithm import *

import random
import warnings
import numpy
warnings.filterwarnings("ignore")

from utils import LoggerManager
logger = LoggerManager().getLogger()

class MonteCarlo(AlgorithmImpl):
    
    def __init__(self, canvas, discount=0.9, iterations=20, episodes=1, plot_policies=False):
        AlgorithmImpl.__init__(self, canvas, discount, iterations, plot_policies)
        self.episodes = episodes
        self.samplings_rewards = [[[] for _ in range(self.canvas.ncols)] for _ in range(self.canvas.nrows)]

    def generate_episode(self):
        '''
        Éste método genera un episodio aleatoriamente. Un episodio es una lista de triplas
        <estado, acción, recompensa>.
        '''
        episode = []
        done = False
        while not done:
            action = random.choice(self.canvas.get_possible_actions(self.canvas.state))
            self.canvas.do_action(action)
            reward = self.canvas.values_board[self.canvas.state[0]][self.canvas.state[1]]
            if reward != 0:
                done = True
            if reward == None:
                reward = 0
            episode += [(self.canvas.state, action, reward), ]
        self.canvas.reset()
        return episode
    

    def calculate_rewards(self, episode):
        '''
        Calcula las recompensas para un episodio dado y la añade a la lista de recompensas
        observadas para cada estado. Ademas, actualiza la tabla de q-valores con los promedios
        de las recompensas observadas para cada estado. 
        '''
        G = 0
        for step in reversed(episode):
            (state, action, reward) = step
            G = self.discount * G + reward
            self.samplings_rewards[state[0]][state[1]].append(G)
            self.q_values[state[0]][state[1]] = numpy.mean(self.samplings_rewards[state[0]][state[1]])


    def monte_carlo(self):
        '''
        Ejecuta el método de Monte Carlo para obtener la política óptima a partir de una
        fase de muestreo. 
        '''

        self.q_values = [[self.canvas.values_board[i][j] for j in range(self.canvas.ncols)] for i in range(self.canvas.nrows)]

        # Inicializo la tabla de políticas vacía.
        self.policy = [[None for j in range(self.canvas.ncols)] for i in range(self.canvas.nrows)]

        # Fase de muestreo. Calculamos los q-valores a partir de la exploración del ambiente
        # durante los episodios generados aleatoriamente. 
        for _ in range(self.episodes):
            episode = self.generate_episode()
            self.calculate_rewards(episode)

            # TODO: Convergencia

        # Fase de extracción de la política. Una vez la fase de muestreo terminada, podemos
        # extraer la política a partir de los q-valores obtenidos. 
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

        # Una vez terminada la ejecucíon del algoritmo, podemos actualizar el canvas
        # con los valores encontrados durante el algoritmo. Esto se hace simplemente
        # para poder visualizar los valores en el canvas.
        self.canvas.values_board = [[self.q_values[i][j] for j in range(self.canvas.ncols)] for i in range(self.canvas.nrows)]
            


    def run(self):
        '''
        Ejectuta el algoritmo. En este caso, lanza el algoritmo basado en el método de Monte Carlo
        que encuentra la mejor política.
        '''
        logger.info('Ejecutando MONTE_CARLO para resolver el MDP')
        required_iterations = self.monte_carlo()
        logger.info(f'La ejecución de MONTE_CARLO acaba de terminar. {required_iterations} fueron necesarias para alcanzar convergencia')

