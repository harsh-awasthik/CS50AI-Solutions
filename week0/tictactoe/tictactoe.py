"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    countX = 0
    countO = 0
    for row in range(3):
        for coloumn in range(3):
            if board[row][coloumn] == X:
                countX += 1
            elif board[row][coloumn] == O:
                countO += 1

    if countX == countO:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for row in range(3):
        for coloumn in range(3):
            if board[row][coloumn] == None:
                actions.add((row, coloumn))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    temp = copy.deepcopy(board)

    cond = action[0] < 0 or action[0] > 2 or action[1] < 0 or action[1] > 2 or (board[action[0]][action[1]] != None)
    if cond:
        raise Exception

    if player(temp) == X:
        temp[action[0]][action[1]] = X
    else:
        temp[action[0]][action[1]] = O

    return temp

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    d1 = []
    d2 = []
    xrow = [X]*3
    orow = [O]*3

    for i in range(3):
        # Checking Horizontally
        if board[i] == xrow:
            return X
        elif board[i] == orow:
            return O

        # Checking Vertically:
        if board[0][i] == board[1][i] == board[2][i]:
            if board[0][i] == X:
                return X
            elif board[0][i] == O:
                return O

        # Checking Diagonally:
        d1.append(board[i][i])
        d2.append(board[i][-i-1])

    if d1 == xrow or d2 == xrow:
        return X
    elif d1 == orow or d2 == orow:
        return O

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True

    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board)

    if w == X:
        return 1
    elif w == O:
        return -1
    else:
        return 0



def minvalue(board):
    if terminal(board):
        return utility(board)

    actionsarr = list(actions(board))
    a = 3
    for action in actionsarr:
        a = min(a, maxvalue(result(board, action)))
    return a

def maxvalue(board):
    if terminal(board):
        return utility(board)

    actionsarr = list(actions(board))
    a = -3
    for action in actionsarr:
        a = max(a, minvalue(result(board, action)))
    return a


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    # Max Conditon
    actionsarr = list(actions(board))
    ans = None
    if player(board) == X:
        a = -3
        for action in actionsarr:
            temp = minvalue(result(board, action))
            if temp > a:
                a = temp
                ans = action

    elif player(board) == O:
        a = 3
        for action in actionsarr:
            temp = maxvalue(result(board, action))
            if temp < a:
                a = temp
                ans = action
    return ans


