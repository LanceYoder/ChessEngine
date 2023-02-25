import chess
import numpy as np

from conversions import *
from piece_maps import *

def evalPos(board):
    #print("______________________")
    #white is going, so board.turn=False
    evaluation = 0

    # randomization so it doesn't just play rook moves when stuck
    # this shouldn't be necessary if my eval is good
    # but it might help make things interesting
    evaluation += np.random.rand()

    if board.is_checkmate():
        evaluation += 1000

    if board.turn:  # if black is going (so now it is white's "turn"), invert check scores
        evaluation *= -1

    # mobility
    evaluation -= board.legal_moves.count() / 60

    # bishop pair
    if board.pieces(chess.BISHOP, not board.turn):
        evaluation += 5



    pieces = board.piece_map()
    for p in pieces:
        piece_type = str(pieces[p])
        # piece weights
        evaluation += pieceToScore(piece_type)
        # piece-square evaluation
        evaluation += pms(piece_type, p)

    return evaluation * -1
