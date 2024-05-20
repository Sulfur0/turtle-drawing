
from enum import Enum

class Size(Enum):
    S = 1
    M = 2
    L = 3


class Rewards:


    def square(self, size=Size.S, single_trace=False):
        '''
        Retorna un tablero con las recompensas necesarias para dibujar un 
        cuadrado. El tablero tiene dimensiones de 100x100. El cuadrado está
        centrado en el tablero. y tiene dimensiones de 80x80. 

        Entradas:
        ----------------
        - size: Define el tamaño del cuadrado. Opciones: S, M, L
        - single_trace: Valor de verdad que indica si se debe retornar un 
          sistema de recompensas para toda la figura o si se debe retornar un
          sistema de recompensas por cada trazo.
        '''

        boards = []

        rows = 0
        columns = 0
        x = 0
        y = 0

        if size == Size.S:
            rows = 5
            columns = 5
            x = 1
            y = 3
        elif size == Size.M:
            rows = 10
            columns = 10
            x = 3
            y = 7
        elif size == Size.L:
            rows = 50
            columns = 50
            x = 5
            y = 45

        if single_trace:
            board = self.empty_board(rows, columns)
            for i in range(rows):
                for j in range(columns):
                    if i == x and j >= x and j <= y:
                        board[i][j] = '+1'
                    if i == y and j >= x and j <= y:
                        board[i][j] = '+1'
                    if j == y and i >= x and i <= y:
                        board[i][j] = '+1'
                    if j == x and i >= x and i <= y:
                        board[i][j] = '+1'

            board[0][0] = 'S'
            boards += [board, ]
        
        else:
            for _ in range(5):
                board = self.empty_board(rows, columns)
                boards += [board, ]
            
            boards[0][0][0] = 'S'
            boards[0][x][x] = '+1'

            boards[1][x][x] = 'S'
            boards[1][x][y] = '+1'

            boards[2][x][y] = 'S'
            boards[2][y][y] = '+1'

            boards[3][y][y] = 'S'
            boards[3][y][x] = '+1'

            boards[4][y][x] = 'S'
            boards[4][x][x] = '+1'

        return boards
    

    def empty_board(self, rows, columns):
        return [[' ' for _ in range(columns)] for _ in range(rows)]
    


