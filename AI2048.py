import numpy as np
from game2048 import *


class AI:

    def __init__(self, board):
        self.board = board
        self.score = 0
        self.depth = 0
        self.max_depth = 1
        self.best_move = None


    def add_tile(self):
        nowBoardR = update_board(self.board, 'r')
        nowBoardL = update_board(self.board, 'l')
        nowBoardU = update_board(self.board, 'u')
        nowBoardD = update_board(self.board, 'd')
        for i in range(4):
            for j in range()
