from AI2048 import AI
from game2048 import *

def main():
    # This function runs the game
    # Input: None
    # Output: None
    game_ai = AI(1)
    board = np.zeros((4, 4))
    board = add_tile(board)
    board = add_tile(board)
    f = Figlet(font='alligator')
    print(f.renderText('2 0 4 8'))
    print("Use WASD to move the tiles.")
    print("Example: W moves the tiles up. Press Enter after your input to make your move")
    print("Type Q to quit the game.")

    input("Press Enter to start the game...")
    print_pretty(board.astype(int).astype(str))
    score = 0
    while True:
        if check_game_over(board):
            print('Game over')
            break
        #inp = str(input()).lower()
        inp = game_ai.get_move(board)
        if inp == 'q':
            print("Quitting game...")
            print("Final score: ", int(score))
            print("Thanks for playing!")
            break
        newBoard, updated, scoreTurn = update_board(board, inp)
        if updated == True:
            board = add_tile(newBoard)
            print_pretty(board.astype(int).astype(str))
            score += scoreTurn
            print("Score: ", int(score))
            print(inp)
        else:
            print('Invalid move')


main()