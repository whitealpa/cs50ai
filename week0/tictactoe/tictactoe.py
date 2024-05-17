"""
Tic Tac Toe Player
"""

import math

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
    
    x_moves = sum(row.count(X) for row in board)
    o_moves = sum(row.count(O) for row in board)
    
    return O if x_moves > o_moves else X
                

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    
    possible_moves = set()
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_moves.add((i, j))  
    
    return possible_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    i, j = action
    
    # Check for out-of-bound moves
    if not (0 <= i < 3 and 0 <= j < 3):
        raise Exception("Out-of-bound moves")
    
    # Deep copy the board
    new_board = [row[:] for row in board] 

    # Check if move is valid
    if new_board[i][j] != EMPTY:
        raise Exception("Invalid move.")
    else:
        new_board[i][j] = player(board)
        return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    # Check for winner (3 in a row or column)
    for i in range(3):
        
        # Check row
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != None:
            return board[i][0] 
        # Check column
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != None:
            return board[0][i]
        
    # Check diagonal
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != None:
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0] and board[0][2]:
        return board[0][2]
        
    # If no winner, return None
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # If there's a winner, game is over
    if winner(board):
        return True
    
    # If there is still an empty cell, game is not over
    for row in board:
        for move in row:
            if move == EMPTY:    
                return False
    
    # Return True if all cells have been filled
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0
    

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    if terminal(board):
        return None

    if player(board) == X:
        beta = float("-inf")
        for action in actions(board):
            value = min_value(result(board, action))
            
            # Condition to find the highest value possible from all possible actions
            if value == 1:
                return action
            elif value > beta:
                beta = value
                move = action
    else:
        alpha = float("inf")
        for action in actions(board):
            value = max_value(result(board, action))

            # Condition to find the lowest value possible from all possible actions
            if value == -1:
                return action
            elif value < alpha:
                alpha = value
                move = action
                
    return move


def max_value(board):

    value = float("-inf")
    
    if terminal(board):
        return utility(board)

    for action in actions(board):
        value = max(value, min_value(result(board, action)))
    return value


def min_value(board):
    
    value = float("inf")
    
    if terminal(board):
        return utility(board)

    for action in actions(board):
        value = min(value, max_value(result(board, action)))
    return value