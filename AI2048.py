import numpy as np
from game2048 import *




class AI:

    def __init__(self, board):
        self.board = board
        self.score = 0
        self.depth = 0
        self.max_depth = 1
        self.best_move = None


    def maximize(self, depth, board):
        moves = ['w', 'a', 's', 'd']
        scores = np.zeros(4)
        for i in range(4):
            new_board, updated, score  = update_board(self.board, moves[i])
            
            if not updated:
                continue

             
            for j in range(4):
                for k in range(4):
                    if new_board[j,k] == 0:
                        new_board[j,k] = 2
                        if depth < self.max_depth:
                            scores, self.maximize(depth + 1, new_board)
                        else:
                            scores[i] =+ self.evaluate(new_board)
                        new_board[j,k] = 4
                        if depth < self.max_depth:
                            self.maximize(depth + 1, new_board)
                        else:
                            scores[i] =+ self.evaluate_board(new_board)
                        new_board[j,k] = 0
        if depth == 0:
            self.best_move = moves[np.argmax(scores)]

        return np.max(scores)
        