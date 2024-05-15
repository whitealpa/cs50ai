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

    """
    The player function should take a board state as input, 
    and return which player’s turn it is (either X or O).
    
    In the initial game state, X gets the first move. Subsequently, the player alternates with each additional move.    
    
    Any return value is acceptable if a terminal board is provided as input (i.e., the game is already over).
    """
    
    x_moves = sum(row.count(X) for row in board)
    o_moves = sum(row.count(O) for row in board)
    
    return O if x_moves > o_moves else X
                

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    
    """
    The actions function should return a set of all of the possible actions that can be taken on a given board.
    
    Each action should be represented as a tuple (i, j) 
    where i corresponds to the row of the move (0, 1, or 2) 
    and j corresponds to which cell in the row corresponds to the move (also 0, 1, or 2).
    
    Possible moves are any cells on the board that do not already have an X or an O in them.
    
    Any return value is acceptable if a terminal board is provided as input.
    """
    
    possible_moves = set()
    
    for i, row in enumerate(board):
        for j, action in enumerate(row):
            if action == EMPTY:
                possible_moves.add((i, j))
    
    return possible_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    """
    The result function takes a board and an action as input, and should return a new board state, without modifying the original board.
    
    If action is not a valid action for the board, your program should raise an exception.
    
    The returned board state should be the board that would result from taking the original input board, 
    and letting the player whose turn it is make their move at the cell indicated by the input action.
    
    Importantly, the original board should be left unmodified: 
    since Minimax will ultimately require considering many different board states during its computation. 
    This means that simply updating a cell in board itself is not a correct implementation of the result function. 
    You’ll likely want to make a deep copy of the board first before making any changes.
    """
    
    # Check for current player
    current_player = player(board)
    i, j = action
    
    # Deep copy the board
    new_board = [row[:] for row in board] 
    
    # Check if move is valid
    if new_board[i][j] != EMPTY:
        raise Exception("Invalid move.")
    else:
        new_board[i][j] = current_player
    
    return new_board
    


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    """
    The winner function should accept a board as input, and return the winner of the board if there is one.
        
    If the X player has won the game, your function should return X. 
    If the O player has won the game, your function should return O.
    
    One can win the game with three of their moves in a row horizontally, vertically, or diagonally.
    
    You may assume that there will be at most one winner 
    (that is, no board will ever have both players with three-in-a-row, 
    since that would be an invalid board state).
    
    If there is no winner of the game (either because the game is in progress, or because it ended in a tie), 
    the function should return None.
    """
    
    # Check for winner (3 in a row or column)
    for i in range(3):
        
        # Check row
        if board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]
        
        # Check column
        elif board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]
        
    # Check diagonal
    if board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
        
    # If no winner, return None
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    
    """
    The terminal function should accept a board as input, 
    and return a boolean value indicating whether the game is over.

    If the game is over, either because someone has won the game 
    or because all cells have been filled without anyone winning, 
    the function should return True.
    
    Otherwise, the function should return False if the game is still in progress.
    """
    
    # If there's a winner, game is over
    if winner(board) != None:
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
    
    """
    The utility function should accept a terminal board as input and output the utility of the board.
    
    If X has won the game, the utility is 1. 
    If O has won the game, the utility is -1. 
    If the game has ended in a tie, the utility is 0.
    
    You may assume utility will only be called on a board if terminal(board) is True.
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
    
    """
    The minimax function should take a board as input, 
    and return the optimal move for the player to move on that board.
    
    The move returned should be the optimal action (i, j) that is one of the allowable actions on the board. 
    If multiple moves are equally optimal, any of those moves is acceptable.
    
    If the board is a terminal board, the minimax function should return None.
    """
    
    if terminal(board):
        return None
    

def main():
    board = initial_state()
    
    print(winner(board))
    

if __name__ == "__main__":
    main()