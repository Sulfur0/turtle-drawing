import random
import numpy
import copy
from algorithm import *

import warnings
warnings.filterwarnings("ignore")

from utils import LoggerManager
logger = LoggerManager().getLogger()

class QLearning(AlgorithmImpl):

    def __init__(self, canvas, discount=0.9, iterations=500, epsilon=0.9, episodes=100, plot_policies=False):
        '''
        Inicializa el algoritmo con los parámetros necesarios. 
        '''
        AlgorithmImpl.__init__(self, canvas, discount, iterations, plot_policies)
        self.qtable = dict()
        self.epsilon = epsilon
        self.alpha = 0.1
        self.gamma = 0.9
        self.episodes = episodes
        for i in range(self.canvas.nrows):
            for j in range(self.canvas.ncols):
                state = (i, j)
                self.qtable[state] = numpy.zeros(len(self.canvas.actions))
    

    def q_learning(self):
        '''
        Éste método ejecuta el algoritmo de Q-learning para calcular la política óptima del MDP. 
        En este caso, el MDP se compone del canvas y la tortuga.
        '''

        # Loop: Iteramos sobre los episodios.
        for episode in range(self.episodes):

            done = False
            while not done:
                current_state = copy.deepcopy(self.canvas.get_current_state())

                # Usamos la estrategia ɛ-decay para seleccionar la siguiente acción del
                # episodio actual.
                if random.uniform(0,1) < self.epsilon:
                    action = self.random_action(current_state)
                else:
                    action = self.max_action(current_state)

                action_index = self.action_index(action)

                # El agente avanza en la dirección dictada por la acción seleccionada anteriormente.
                next_state, reward, done = self.step(action)

                # Actualizamos el q-valor del siguiente estado.
                if not done:
                    next_max = numpy.max(self.qtable[next_state])
                    self.qtable[current_state][action_index] = (1 - self.alpha) * self.qtable[current_state][action_index] + self.alpha * (reward + self.gamma * next_max)
                else:
                    self.qtable[current_state][action_index] = reward

            if episode % 30 == 0:
                self.epsilon -= self.epsilon / 10
                
            self.canvas.reset()

        return self.qtable
                
    
    def step(self, action):
        old_state = copy.deepcopy(self.canvas.get_current_state())
        reward, new_state = self.canvas.do_action(action)
        next_state = copy.deepcopy(new_state)
        return next_state, reward, self.canvas.is_terminal()

    
    def random_action(self, state):
        '''
        Selecciona una acción de manera aleatoria entre las posibles acciones del agente
        a partir del estado dado.
        '''
        return random.choice(self.canvas.get_possible_actions(state))
    

    def max_action(self, state):
        '''
        Retorna la mejor acción para el estado dado con respecto a la tabla de q-valores.
        '''
        action_index = numpy.argmax(self.qtable[state]) 
        actions = self.canvas.actions
        return actions[action_index]
    

    def action_index(self, action):
        '''
        Retorna el índice correspondiente a la acción dada en el parámetro.
        '''
        actions = self.canvas.actions
        for i in range(len(actions)):
            if actions[i] == action:
                return i
        return -1
    

    def actions_values(self):
        '''
        Retorna una tupla acciones-valor que permite asociar cada acción a su q-valor correspondiente.
        '''
        actions = {}
        self.canvas.reset()

        values = dict()
        for i in range(self.canvas.nrows):
            for j in range(self.canvas.ncols):
                state = (i, j)
                values[state] = 0
        
        for i in range(self.canvas.nrows):
            for j in range(self.canvas.ncols):
                state = (i, j)
                action = numpy.argmax(self.qtable[state]) 
                actions[state] = self.canvas.actions[action]
                values[state] = numpy.max(self.qtable[state])
        return actions, values
    


    def run(self):
        '''
        Ejectuta el algoritmo. En este caso, lanza el algoritmo de 'policy_iteration'
        que encuentra la mejor política.
        '''
        logger.info('Ejecutando Q_LEARNING para resolver el MDP')
        self.q_learning()
        logger.info(f'La ejecución de Q_LEARNING acaba de terminar. {self.episodes} fueron necesarias para alcanzar convergencia')
