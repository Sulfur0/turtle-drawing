import random

#PolicyIteraction
class PolicyIteration():
    
    #1
    def __init__(self, mdp, discount=0.9, iterations=500):
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = [[self.mdp.grid[i][j] for j in range(self.mdp.ncols)] for i in range(self.mdp.nrows)]
        self.policy = [[random.choice(self.mdp.get_possible_actions((i, j))) if self.mdp.grid[i][j] != None else None for j in range(self.mdp.ncols)] for i in range(self.mdp.nrows)]
        #self.policy = [['up' if self.mdp.grid[i][j] != None and self.mdp.grid[i][j] != 1 and self.mdp.grid[i][j] != -1 else None for j in range(self.mdp.ncols)] for i in range(self.mdp.nrows)]
    
    #2 
    def get_policy(self, state):
        i, j = state
        return self.policy[i][j]
    
    #3
    def get_value(self, state):
        i, j = state
        return self.values[i][j]
    
    #3
    def compute_new_value_from_values(self, state, action):
        t = 1 # El ruido es 0 dado que el MDP es deterministico. Entonces t = 1 siempre
        reward, state_prime = self.mdp.do_action(action)
        #if self.mdp.actions_collide(self.get_policy(state), self.get_policy(state_prime)):
        #    return -1000
        if self.positive_reward(state) and self.positive_reward(state_prime): # Jackspot! The value from this action is a positive reward!
            return 1000
        return t * (self.mdp.grid[state[0]][state[1]] + self.discount * self.get_value(state_prime))
    
    def positive_reward(self, state) -> bool:
        return self.get_value(state) == 1 or self.get_value(state) == 10

    #7
    def policy_evaluation(self):
        for i in range(self.mdp.nrows):
            for j in range(self.mdp.ncols):
                state = (i, j)
                if self.mdp.grid[i][j] != None:
                    self.mdp.state = state
                    if not self.mdp.is_terminal():
                        # Calculo la ecuación de Bellman para cada uno de los estados a los que puedo llegar
                        # con las acciones válidas desde el estado actual. 
                        action = self.get_policy(state)
                        self.values[i][j] = self.compute_new_value_from_values(state, action)
                        self.mdp.state = state                        
                        
    
    #8
    def policy_iteration(self):
        # Loop: para cada iteración k
        for iteration in range(self.iterations):
            # Loop: para cada estado s
            self.policy_evaluation()
            for i in range(self.mdp.nrows):
                for j in range(self.mdp.ncols):
                    state = (i, j)
                    if self.mdp.grid[i][j] != None:
                        self.mdp.state = state
                        best_action = self.get_policy(state)
                        best_value = self.values[i][j]
                        for action in self.mdp.get_possible_actions(state):
                            new_value = self.compute_new_value_from_values(state, action)
                            self.mdp.do_action(action)
                            if new_value > best_value:
                                best_value = new_value
                                if self.values[i][j] != -1 and not self.positive_reward(state=(i, j)):
                                    self.values[i][j] = new_value
                                best_action = action
                            self.mdp.state = state
                            
                        self.policy[i][j] = best_action


        self.mdp.grid = [[self.values[i][j] for j in range(self.mdp.ncols)] for i in range(self.mdp.nrows)]