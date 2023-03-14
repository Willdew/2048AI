import numpy as np
import random


def updateBoard(board, input):
    # This function updates the board after each move
    # and returns the updated board
    # Input: 4x4 numpy array
    # Output: 4x4 numpy array
    newBoard = board
    score = 0
    if input == 'w' or input == 's':
        newBoard, score = moveVert(board, input)
    elif input == 'a' or input == "d":
        newBoard, score = moveHori(board, input)
    if np.array_equal(newBoard, board) == False:
        return newBoard, True, score
    return board, False, score

def moveVert(board, input):
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

def moveHori(board, input):
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


def addTile(board):
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

def printBoard(board):
    # This function prints the board
    # Input: 4x4 numpy array
    # Output: None
    for i in range(4):
        print(end='|')
        for j in range(4):
            if board[i, j] == 0:
                
                print('   ', end='   ')
            else:
                print('  ', board[i, j], end='  ')
        print()


def checkGameOver(board):
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

def main():
    # This function runs the game
    # Input: None
    # Output: None
    board = np.zeros((4, 4))
    board = addTile(board)
    board = addTile(board)
    print("Use WASD to move the tiles.")
    print("Example: W moves the tiles up. Press Enter after your input to make your move")
    print("Type Q to quit the game.")
    printBoard(board.astype(int))
    score = 0
    while True:
        if checkGameOver(board):
            print('Game over')
            break
        inp = str(input()).lower()
        if inp == 'q':
            print("Quitting game...")
            print("Final score: ", int(score))
            print("Thanks for playing!")
            break
        newBoard, updated, scoreTurn = updateBoard(board, inp)
        if updated == True:
            board = addTile(newBoard)
            printBoard(board.astype(int))
            score += scoreTurn
            print("Score: ", int(score))
        else:
            print('Invalid move')

main()
