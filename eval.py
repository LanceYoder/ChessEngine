import chess
import numpy as np

from conversions import *
from piece_maps import *

def evalPos(board, colorWhite):
    #print("______________________")
    #white is going, so board.turn=False
    evaluation = 0



    #if board.turn then black wants a good score
    #if not board.turn then white wants a good score

    # randomization so it doesn't just play rook moves when stuck
    # this shouldn't be necessary if my eval is good
    # but it might help make things interesting
    evaluation += np.random.rand()

    # if
    if board.is_checkmate():
        if board.turn:
            evaluation -= 100000
        else:
            evaluation += 100000

    # mobility
    evaluation -= board.legal_moves.count() / 6

    # bishop pair
    if board.pieces(chess.BISHOP, not board.turn):
        evaluation += 50

    pieces = board.piece_map()
    for p in pieces:
        piece_type = str(pieces[p])
        # piece weights
        evaluation += pieceToScore(piece_type)
        # piece-square evaluation
        evaluation += pms(piece_type, p)
    #print(str(evaluation))

    return evaluation if colorWhite else -1 * evaluation

# return an int indicating game phase
# 0-100, 0 being opening, 100 being endgame
def game_phase(board):
    phase = 0
    pieces = board.piece_map()
    phase += (32 - len(pieces)) * 3
    if not board.has_castling_rights(chess.WHITE):
        phase += 5
    if not board.has_castling_rights(chess.BLACK):
        phase += 5

    if len(board.pieces(chess.QUEEN, chess.WHITE)) + len(board.pieces(chess.QUEEN, chess.BLACK)) == 0:
        phase += 10
