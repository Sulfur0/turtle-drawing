import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Canvas:
    '''
    Esta clase representa el tablero con la solución al MDP. Recibe el tablero con las recompensas
    y lo usa como el punto de partida para calcular los valores de cada estado con respecto a una política.
    '''

    def __init__(self, rewards_board):
    
        self.nrows, self.ncols = len(rewards_board),len(rewards_board[0])
        self.dimensions = (self.nrows, self.ncols)
        self.values_board = [[None for _ in range(self.ncols)] for _ in range(self.nrows)]

        for i in range(self.nrows):
            for j in range(self.ncols):
                cell = rewards_board[i][j]
                if cell == ' ' :
                    self.values_board[i][j] = 0
                elif cell == '#' :
                    self.values_board[i][j] = None
                elif cell == 'S' :
                    self.state = (i, j)
                    self.initial_state = (i, j)
                    self.values_board[i][j] = 0
                else :
                    self.values_board[i][j] = int(cell)


    def get_current_state(self):
        '''
        Retorna el estado actual del canvas. 
        '''
        return self.state
    

    def actions_collide(self, source_action, target_action):
        if source_action == 'up' and target_action == 'down':
            return True
        if source_action == 'down' and target_action == 'up':
            return True
        if source_action == 'left' and target_action == 'right':
            return True
        if source_action == 'right' and target_action == 'left':
            return True
        return False
    
    def get_opposite(self, action):
        if action == 'up':
            return 'down'
        if action == 'down':
            return 'up'
        if action == 'left':
            return 'right'
        if action == 'right':
            return 'left'
        

    def get_possible_actions(self, state):
        actions = []

        # El agente se puede mover hacia arriva si se encuentra en
        # la fila 1 o más abajo y si no hay un obstáculo en la casilla de arriba.
        # Sabemos que hay un obstáculo cuando la recompensa es 'None'.
        if state[0] > 0 and self.values_board[state[0] - 1][state[1]] != None:
            actions += ['up',]

        # El agente se puede mover hacia abajo si se encuentra en
        # la penutltima fila o más arriba y si no hay un obstáculo en la casilla de arriba.
        # Sabemos que hay un obstáculo cuando la recompensa es 'None'.
        if state[0] < self.nrows - 1 and self.values_board[state[0] + 1][state[1]] != None:
            actions += ['down',]

        # El agente se puede mover hacia la izquierda si se encuentra en
        # la primera columna o más hacia la derecha y si no hay un obstáculo en la casilla de la izquierda.
        # Sabemos que hay un obstáculo cuando la recompensa es 'None'.
        if state[1] > 0  and self.values_board[state[0]][state[1] - 1] != None:
            actions += ['left',]

        # El agente se puede mover hacia la derecha si se encuentra en
        # la penutltima columna o más hacia la izquierda y si no hay un obstáculo en la casilla la derecha.
        # Sabemos que hay un obstáculo cuando la recompensa es 'None'.
        if state[1] < self.ncols - 1 and self.values_board[state[0]][state[1] + 1] != None:
            actions += ['right',]

        return actions
    

    def do_action(self, action):
        if action in self.get_possible_actions(self.state):
            new_state = None
            if action == 'up':
                new_state = (self.state[0] - 1, self.state[1])
            elif action == 'down':
                new_state = (self.state[0] + 1, self.state[1])
            elif action == 'right':
                new_state = (self.state[0], self.state[1] + 1)
            elif action == 'left':
                new_state = (self.state[0], self.state[1] - 1)
            self.state = new_state

        return self.values_board[self.state[0]][self.state[1]], self.state

    #5
    def reset(self):
        self.state = self.initial_state
    
    #6
    def is_terminal(self, state=None):
        if state == None:
            state = self.state
        i, j = state
        if i >= len(self.values_board) or j >= len(self.values_board[0]):
            return False
        else:
            return self.values_board[i][j] in [1, 10, 20, 200, 800, 2000, 3000, 4000]


    def plot_rainbow(self):
        fig1 = plt.figure(figsize=(15, 15))
        ax1 = fig1.add_subplot(111, aspect='equal')
        
        # Lineas
        for i in range(0, len(self.values_board)+1):
            ax1.axhline(i , linewidth=2, color="#2D2D33")
        for i in range(len(self.values_board[0])+1):
            ax1.axvline(i , linewidth=2, color="#2D2D33")
        
        # Amarillo - inicio
        (i,j)  = self.initial_state
        ax1.add_patch(patches.Rectangle((j, self.nrows - i -1), 1, 1, facecolor = "#F6D924"))
        for j in range(len(self.values_board[0])):
            for i in range(len(self.values_board)):
                if self.is_terminal(state=(i, j)): # verde
                    ax1.add_patch(patches.Rectangle((j,self.nrows - i -1), 1, 1, facecolor = "#68FF33"))
                elif self.values_board[i][j] < 0: # rojo
                    ax1.add_patch(patches.Rectangle((j,self.nrows - i -1), 1, 1, facecolor = "#f0837f"))
                elif self.values_board[i][j] >= 0 and self.values_board[i][j] < 3: #amarillo
                    ax1.add_patch(patches.Rectangle((j,self.nrows - i -1), 1, 1, facecolor = "#eef593"))
                elif self.values_board[i][j] >= 3 and self.values_board[i][j] < 5: #verde claro
                    ax1.add_patch(patches.Rectangle((j,self.nrows - i -1), 1, 1, facecolor = "#cdf7b5"))
                elif self.values_board[i][j] >= 5 and self.values_board[i][j] < 10: #verde claro
                    ax1.add_patch(patches.Rectangle((j,self.nrows - i -1), 1, 1, facecolor = "#b7f792"))
                elif self.values_board[i][j] >= 10: #verde mas oscuro
                    ax1.add_patch(patches.Rectangle((j,self.nrows - i -1), 1, 1, facecolor = "#9cf768"))
                

        for i in range(len(self.values_board)):
            for j in range(len(self.values_board[0])):
                if self.values_board[i][j] == None:
                    ax1.text(self.ncols-j-1, self.nrows-i-1, "", ha='center', va='center', fontsize=6)
                else:
                    ax1.text(j+0.5, self.nrows-i-1+0.5, str(round(self.values_board[i][j], 1)), ha='center', va='center', fontsize=6)
        plt.axis("off")
        plt.show()

    
    def print_policy(self, i, j, policy):
        if policy[i][j] == "up":
            return "^"
        elif policy[i][j] == "down":
            return "⌄"
        elif policy[i][j] == "left":
            return "<"
        elif policy[i][j] == "right":
            return ">"
        return ""
    

    def plot_policy(self, policy):
        fig1 = plt.figure(figsize=(15, 15))
        ax1 = fig1.add_subplot(111, aspect='equal')
        
        # Lineas
        for i in range(0, len(self.values_board)+1):
            ax1.axhline(i , linewidth=2, color="#2D2D33")
        for i in range(0, len(self.values_board[0])+1):
            ax1.axvline(i , linewidth=2, color="#2D2D33")
        
        # Amarillo - inicio
        (i,j)  = self.initial_state
        ax1.add_patch(patches.Rectangle((j, self.nrows - i -1), 1, 1, facecolor = "#F6D924"))
        for j in range(len(self.values_board[0])):
            for i in range(len(self.values_board)):
                if self.is_terminal(state=(i, j)): # verde
                    ax1.add_patch(patches.Rectangle((j,self.nrows - i -1), 1, 1, facecolor = "#68FF33"))
                if self.values_board[i][j] == None: # gris
                    ax1.add_patch(patches.Rectangle((j,self.nrows - i -1), 1, 1, facecolor = "#6c7780"))
                if self.values_board[i][j] == -1: # rojo
                    ax1.add_patch(patches.Rectangle((j,self.nrows - i -1), 1, 1, facecolor = "#cc0000"))

        for i in range(len(self.values_board)):
            for j in range(len(self.values_board[0])):
                if self.values_board[i][j] == None:
                    ax1.text(self.ncols-j-1, self.nrows-i-1, "", ha='center', va='center', fontsize=6)
                else:
                    ax1.text(j+0.5, self.nrows-i-1+0.5, self.print_policy(i,j, policy), ha='center', va='center', fontsize=6)
        plt.axis("off")
        plt.show()