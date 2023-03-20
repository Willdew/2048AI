import numpy as np
import random

from rich import box
from rich.table import Table
from rich.console import Console
from pyfiglet import Figlet


def update_board(board, input):
    # This function updates the board after each move
    # and returns the updated board
    # Input: 4x4 numpy array
    # Output: 4x4 numpy array
    newBoard = board
    score = 0
    if input == 'w' or input == 's':
        newBoard, score = move_vert(board, input)
    elif input == 'a' or input == "d":
        newBoard, score = move_horizontal(board, input)
    if np.array_equal(newBoard, board) == False:
        return newBoard, True, score
    return board, False, score


def move_vert(board, input):
    newBoard = np.zeros((4, 4))
    if input == 's':
        board = np.flipud(board)
    score = 0
    for i in range(4):
        col = board[:, i]
        newCol = np.zeros(4)
        ind = 0
        multi = False

        for j in range(4):
            if col[j] != 0:
                if ind != 0 and newCol[ind - 1] == col[j] and multi == False:
                    newCol[ind - 1] = 2 * col[j]
                    multi = True
                    score = score + 2 * col[j]
                elif col[j] != 0:
                    newCol[ind] = col[j]
                    ind += 1
                    multi = False
        newBoard[:, i] = newCol
    if input == 's':
        newBoard = np.flipud(newBoard)
    return newBoard, score


def move_horizontal(board, input):
    newBoard = np.zeros((4, 4))
    if input == 'd':
        board = np.fliplr(board)
    score = 0
    for i in range(4):
        row = board[i, :]
        newRow = np.zeros(4)
        ind = 0
        multi = False
        for j in range(4):
            if row[j] != 0:
                if ind != 0 and newRow[ind - 1] == row[j] and multi == False:
                    newRow[ind - 1] = 2 * row[j]
                    score += 2 * row[j]
                    multi = True
                elif row[j] != 0:
                    newRow[ind] = row[j]
                    ind += 1
                    multi = False
        newBoard[i, :] = newRow
    if input == 'd':
        newBoard = np.fliplr(newBoard)
    return newBoard, score


def add_tile(board):
    # This function adds a tile to the board
    # Input: 4x4 numpy array
    # Output: 4x4 numpy array
    newBoard = board
    if np.count_nonzero(board) == 16:
        return newBoard
    while True:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row, col] == 0:
            newInt = random.random()
            if newInt < 0.9:
                newBoard[row, col] = 2
            else:
                newBoard[row, col] = 4
            break
    return newBoard


def check_game_over(board):
    # This function checks if the game is over
    # Input: 4x4 numpy array
    # Output: Boolean

    if np.count_nonzero(board) == 16:
        for i in range(4):
            for j in range(4):
                if i != 3 and board[i, j] == board[i + 1, j]:
                    return False
                if j != 3 and board[i, j] == board[i, j + 1]:
                    return False
        return True
    else:
        return False


def print_pretty(board):
    # Replace 0 with a space in board
    board[board == "0"] = ' '
    table = Table(box=box.ROUNDED, show_header=False, show_lines=True, style="magenta", highlight=True, expand=True)
    board_list = board.tolist()

    for row in board_list:
        table.add_row(*row)

    console = Console()
    console.clear()
    f = Figlet(font='alligator')
    console.clear()
    console.print(f"[cyan]{f.renderText('2 0 4 8')}[/cyan]")
    console.print(table)


def main():
    # This function runs the game
    # Input: None
    # Output: None
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
        inp = str(input()).lower()
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
        else:
            print('Invalid move')


main()