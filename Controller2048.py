import numpy as np

from AI2048 import AI
from game2048 import *
import multiprocessing as mp
import warnings
warnings.filterwarnings(action='ignore', category=RuntimeWarning)

def take_turn(board, move, score):

    if check_game_over(board):
        return board, score, True

    if move == 'q':
        return board, score, True

    newBoard, updated, scoreTurn = update_board(board, move)
    if updated == True:
        board = add_tile(newBoard)
        score += scoreTurn
        return board, score, False

    else:
        print('Invalid move')
        return board, score, False

def start_game():
    board = np.zeros((4, 4))
    board = add_tile(board)
    board = add_tile(board)
    return board

def game_loop(game_ai, print_board=True):
    board = start_game()
    score = 0
    game_over = False
    while(game_over == False):
        move = game_ai.get_move(board)
        board, score, game_over = take_turn(board, move, score)
        if print_board:
            print_pretty(board.astype(int).astype(str))
            print("Score: ", int(score))

    max_tile = np.max(board)
    return score, max_tile




def main():
    # This function runs the game
    # Input: None
    # Output: None
    game_ai = AI(1)
    f = Figlet(font='alligator')
    print(f.renderText('2 0 4 8'))
    print("Use WASD to move the tiles.")
    print("Example: W moves the tiles up. Press Enter after your input to make your move")
    print("Type Q to quit the game.")
    score = 0
    inp = input("Press Enter to start the game or b to benchmark")
    if inp == 'b':
        data_array = np.zeros((4,21))
        for p in range(20):
            game_ai.set_weights(1,p/10)
            score = []
            max_tiles = []
            for i in range(20):
                temp_score, max_tile = game_loop(game_ai, print_board=False)
                score.append(temp_score)
                max_tiles.append(max_tile)
            data_array[p,0] = p/10
            data_array[p,1] = np.mean(score)
            data_array[p,2] = np.std(score)
            data_array[p,3] = np.max(max_tiles)
            data_array[p,4] = np.min(max_tiles)
            data_array[p,5] = np.median(max_tiles)
            print_pretty(data_array.astype(str))




        print("Max tile: ", np.max(max_tiles))
        print("Min tile: ", np.min(max_tiles))
        print("Median tile: ", np.median(max_tiles))
        print("Average score: ", np.mean(score))
        print("Standard deviation: ", np.std(score))
        print("Max score: ", np.max(score))
        print("Min score: ", np.min(score))
        print("Median score: ", np.median(score))





    else:
        game_loop(game_ai)

if __name__ == '__main__':
    main()