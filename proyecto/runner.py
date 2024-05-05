from canvas import Canvas
from policy import PolicyIteration
from logo import Logo

class Drawing:

    def __init__(self):
        self.rows, self.columns = 50, 50

        # Inicializo el tablero con todas las recompensas en cero
        self.board = [[' ' for _ in range(self.columns)] for _ in range(self.rows)]

        # Defino las recompensas de acuerdo a la figura que queremos dibujar.
        for i in range(self.rows):
            for j in range(self.columns):
                if i == 10 and j >= 10 and j <= 40:
                    self.board[i][j] = '+1'
                if i == 40 and j >= 10 and j <= 40:
                    self.board[i][j] = '+1'
                if j == 40 and i >= 10 and i <= 40:
                    self.board[i][j] = '+1'
                if j == 10 and i >= 10 and i <= 40:
                    self.board[i][j] = '+1'

        self.board[0][0] = 'S'
        self.env = Canvas(self.board)

    
    def train(self):
        # Creo el agente obtengo la política que va a guiar la tortuga
        # a lo largo del canvas en su tarea de dibujar.
        agent = PolicyIteration(self.env)
        agent.policy_iteration()
        return agent
    

    def draw_policy(self, agent):
        # Creo la tortuga que que recibe el agente y le pido que empiece
        # el dibujo
        logo = Logo(env=agent.mdp)
        logo.draw(agent)


    def run(self):
        agent = self.train()
        self.draw_policy(agent)


Drawing().run()