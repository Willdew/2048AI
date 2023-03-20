import numpy as np
from game2048 import update_board
import multiprocessing as mp
import time


class AI:

    def __init__(self, max_depth=1):
        self.max_depth = max_depth
        # Sets up multiprocessing
        mp.freeze_support()
        self.zero_weight = 1
        self.edge_weight = 1
        # Spawn starts a new process
        #mp.set_start_method('spawn', force = True)

    def set_max_depth(self, max_depth):
        self.max_depth = max_depth

    def get_max_depth(self):
        return self.max_depth

    def set_weights(self, zero_weight, edge_weight):
        self.zero_weight = zero_weight
        self.edge_weight = edge_weight
    def evaluate_board(self, board):
        score = 0
        edge = 0

        heuristic = [[4 ** 16, 4 ** 15, 4 ** 14, 4 ** 13],
                      [4 ** 10, 4 ** 4, 4 ** 11, 4 ** 12],
                      [4 ** 9, 4 ** 8, 4 ** 7, 4 ** 6],
                      [4 ** 5, 4 ** 4, 4 ** 3, 4 ** 2]]

        for y in range(4):
             for x in range(4):
                 edge += board[x][y] * heuristic[x][y]

        zeros = 16 - np.count_nonzero(board)
        #print("edge: ", np.log(edge))
        #print("zeros: ", zeros)
        score = self.zero_weight * zeros + self.edge_weight * np.log(edge)
        return score

    def maximize(self, board, move, depth=0):
        scores = np.zeros(2)
        new_board, updated, _ = update_board(board, move)

        if not updated:
            return 0

        z = 16 - np.count_nonzero(new_board)
        for j in range(4):
            for k in range(4):
                if new_board[j, k] == 0:
                    new_board[j, k] = 2
                    if depth < self.max_depth:
                        s = self.recurse_board(new_board, depth + 1)
                        scores[0] += s
                    else:
                        scores[0] += self.evaluate_board(new_board)
                    new_board[j, k] = 4
                    if depth < self.max_depth:
                        s = self.recurse_board(new_board, depth + 1)
                        scores[1] += s
                    else:
                        scores[1] += self.evaluate_board(new_board)
                    new_board[j, k] = 0
        scores[0] /= z
        scores[1] /= z


        return scores[0] * 0.9 + scores[1] * 0.1

    def recurse_board(self, board, depth=0):
        moves = ['w', 'a', 's', 'd']
        scores = np.zeros(4)
        for i in range(4):
            scores[i] = self.maximize(board, moves[i], depth)

        return np.mean(scores[scores != 0])


    def get_move(self, board):
        pool = mp.Pool(processes=4)
        moves = ['w', 'a', 's', 'd']
        results = [pool.apply_async(self.maximize, args=(board, move)) for move in moves]
        pool.close()
        pool.join()
        scores = [r.get() for r in results]
        return moves[np.argmax(scores)]
