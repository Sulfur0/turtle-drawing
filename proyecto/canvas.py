import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Canvas:

    def __init__(self, board):
        '''
        Se inicialiaza el tablero sobre el cual se mueve Logo. Este tablero entra por parámetro.
        '''
        self.nrows, self.ncols = len(board),len(board[0])
        self.dimensions = (self.nrows, self.ncols)
        self.grid = [[None for _ in range(self.ncols)] for _ in range(self.nrows)]

        for i in range(self.nrows):
            for j in range(self.ncols):
                cell = board[i][j]
                if cell == ' ' :
                    self.grid[i][j] = 0
                elif cell == '#' :
                    self.grid[i][j] = None
                elif cell == 'S' :
                    self.state = (i, j)
                    self.initial_state = (i, j)
                    self.grid[i][j] = 0
                else :
                    self.grid[i][j] = int(cell)


    #2
    def get_current_state(self):
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
        if state[0] > 0 and self.grid[state[0] - 1][state[1]] != None:
            actions += ['up',]

        # El agente se puede mover hacia abajo si se encuentra en
        # la penutltima fila o más arriba y si no hay un obstáculo en la casilla de arriba.
        # Sabemos que hay un obstáculo cuando la recompensa es 'None'.
        if state[0] < self.nrows - 1 and self.grid[state[0] + 1][state[1]] != None:
            actions += ['down',]

        # El agente se puede mover hacia la izquierda si se encuentra en
        # la primera columna o más hacia la derecha y si no hay un obstáculo en la casilla de la izquierda.
        # Sabemos que hay un obstáculo cuando la recompensa es 'None'.
        if state[1] > 0  and self.grid[state[0]][state[1] - 1] != None:
            actions += ['left',]

        # El agente se puede mover hacia la derecha si se encuentra en
        # la penutltima columna o más hacia la izquierda y si no hay un obstáculo en la casilla la derecha.
        # Sabemos que hay un obstáculo cuando la recompensa es 'None'.
        if state[1] < self.ncols - 1 and self.grid[state[0]][state[1] + 1] != None:
            actions += ['right',]

        return actions
    
    #4
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

        return self.grid[self.state[0]][self.state[1]], self.state

    #5
    def reset(self):
        self.state = self.initial_state
    
    #6
    def is_terminal(self, state=None):
        if state == None:
            state = self.state
        i, j = state
        return self.grid[i][j] in [1, 10, 20, 30, 40]
    
    #Función de soporte para pintar el ambiente
    def plot(self):
        fig1 = plt.figure(figsize=(20, 20))
        ax1 = fig1.add_subplot(111, aspect='equal')
        
        # Lineas
        for i in range(0, len(self.grid)+1):
            ax1.axhline(i , linewidth=2, color="#2D2D33")
        for i in range(len(self.grid[0])+1):
            ax1.axvline(i , linewidth=2, color="#2D2D33")
        
        # Amarillo - inicio
        (i,j)  = self.initial_state
        ax1.add_patch(patches.Rectangle((j, self.nrows - i -1), 1, 1, facecolor = "#F6D924"))
        for j in range(len(self.grid[0])):
            for i in range(len(self.grid)):
                if self.is_terminal(state=(i, j)): # verde
                    ax1.add_patch(patches.Rectangle((j,self.nrows - i -1), 1, 1, facecolor = "#68FF33"))
                if self.grid[i][j] == None: # gris
                    ax1.add_patch(patches.Rectangle((j,self.nrows - i -1), 1, 1, facecolor = "#6c7780"))
                if self.grid[i][j] == -1: # rojo
                    ax1.add_patch(patches.Rectangle((j,self.nrows - i -1), 1, 1, facecolor = "#cc0000"))

        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == None:
                    ax1.text(self.ncols-j-1, self.nrows-i-1, "", ha='center', va='center')
                else:
                    ax1.text(j+0.5, self.nrows-i-1+0.5, str(round(self.grid[i][j],2)), ha='center', va='center')
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
        fig1 = plt.figure(figsize=(20, 20))
        ax1 = fig1.add_subplot(111, aspect='equal')
        
        # Lineas
        for i in range(0, len(self.grid)+1):
            ax1.axhline(i , linewidth=2, color="#2D2D33")
        for i in range(0, len(self.grid[0])+1):
            ax1.axvline(i , linewidth=2, color="#2D2D33")
        
        # Amarillo - inicio
        (i,j)  = self.initial_state
        ax1.add_patch(patches.Rectangle((j, self.nrows - i -1), 1, 1, facecolor = "#F6D924"))
        for j in range(len(self.grid[0])):
            for i in range(len(self.grid)):
                if self.is_terminal(state=(i, j)): # verde
                    ax1.add_patch(patches.Rectangle((j,self.nrows - i -1), 1, 1, facecolor = "#68FF33"))
                if self.grid[i][j] == None: # gris
                    ax1.add_patch(patches.Rectangle((j,self.nrows - i -1), 1, 1, facecolor = "#6c7780"))
                if self.grid[i][j] == -1: # rojo
                    ax1.add_patch(patches.Rectangle((j,self.nrows - i -1), 1, 1, facecolor = "#cc0000"))

        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == None:
                    ax1.text(self.ncols-j-1, self.nrows-i-1, "", ha='center', va='center')
                else:
                    ax1.text(j+0.5, self.nrows-i-1+0.5, self.print_policy(i,j, policy), ha='center', va='center')
        plt.axis("off")
        plt.show()