import numpy as np
from game2048 import *




class AI:

    def __init__(self, board):
        self.board = board
        self.score = 0
        self.depth = 0
        self.max_depth = 1
        self.best_move = None

    def evaluate_board(self, board):
        score = 0

        # Count the number of empty cells on the board
        num_empty = np.sum(board == 0)

        # Score for tiles in same row or column with the same number
        same_row_score = np.sum(np.max(board[:-1, :] == board[1:, :], axis=1))
        same_col_score = np.sum(np.max(board[:, :-1] == board[:, 1:], axis=0))
        score += (same_row_score + same_col_score) * 5

        # Score for order of numbers on board
        sorted_board = np.sort(board, axis=None)[::-1].reshape((4, 4))
        ordered_score = 0
        if sorted_board[0, 3] == np.max(board):
            ordered_score += 10
        for i in range(3):
            for j in range(3):
                if sorted_board[i, j] > sorted_board[i, j + 1] and sorted_board[i + 1, j] > sorted_board[i, j]:
                    ordered_score += 1
        score += ordered_score

        # Penalty for number of empty cells on board
        score += num_empty * 2

        return score

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
        