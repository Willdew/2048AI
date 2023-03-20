import numpy as np
from game2048 import update_board




class AI:

    def __init__(self, max_depth=1):
        self.max_depth = max_depth

    def set_max_depth(self, max_depth):
        self.max_depth = max_depth

    def get_max_depth(self):
        return self.max_depth

    def evaluate_board(self, board):
        # score = 0
        #
        # # Count the number of empty cells on the board
        # num_empty = np.sum(board == 0)
        #
        # # Score for tiles in same row or column with the same number
        # same_row_score = np.sum(np.max(board[:-1, :] == board[1:, :], axis=1))
        # same_col_score = np.sum(np.max(board[:, :-1] == board[:, 1:], axis=0))
        # score += (same_row_score + same_col_score) * 5
        #
        # # Score for order of numbers on board
        # sorted_board = np.sort(board, axis=None)[::-1].reshape((4, 4))
        # ordered_score = 0
        # if sorted_board[0, 3] == np.max(board):
        #     ordered_score += 10
        # for i in range(3):
        #     for j in range(3):
        #         if sorted_board[i, j + 1] < sorted_board[i, j] < sorted_board[i + 1, j]:
        #             ordered_score += 1
        # score += ordered_score
        #
        # # Penalty for number of empty cells on board
        # score += num_empty * 2

        edge_weight = 1
        zero_weight = 1
        score = 0
        edge = 0

        heuristic = [[4 ** 6, 4 ** 5, 4 ** 4, 4 ** 3],
                      [4 ** 5, 4 ** 4, 4 ** 3, 4 ** 2],
                      [4 ** 4, 4 ** 3, 4 ** 2, 4 ** 1],
                      [4 ** 3, 4 ** 2, 4 ** 1, 4 ** 0]]
         # Loops through the board and calculates the heuristic
        for y in range(4):
             for x in range(4):
                 edge += board[x][y] * heuristic[x][y]

        zeros = 16 - np.count_nonzero(board)
        print("edge: ", np.log(edge))
        print("zeros: ", zeros)
        score = edge_weight * edge + zero_weight * zeros
        return score

    def maximize(self, board, depth = 0):
        moves = ['w', 'a', 's', 'd']
        scores = np.zeros(4)
        for i in range(4):
            new_board, updated, _  = update_board(board, moves[i])

            if not updated:
                continue

            z = 16-np.count_nonzero(new_board)
            for j in range(4):
                for k in range(4):
                    if new_board[j,k] == 0:
                        new_board[j,k] = 2
                        if depth < self.max_depth:
                            s, _ =  self.maximize(new_board, depth + 1)
                            scores[i] += s
                        else:
                            scores[i] += self.evaluate_board(new_board)

                        new_board[j,k] = 4
                        if depth < self.max_depth:
                            self.maximize(new_board, depth + 1)
                        else:
                            scores[i] =+ self.evaluate_board(new_board)
                        new_board[j,k] = 0
            scores[i] /= z

        if depth == 0:
            self.best_move = moves[np.argmax(scores)]

        return np.mean(scores[scores != 0]), moves[np.argmax(scores)]
