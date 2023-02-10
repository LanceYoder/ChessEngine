from eval import *

def quiescence(board):
    moves = board.legal_moves

    for i, move in enumerate(moves):
        if board.is_capture(move):
            evalPos(board)