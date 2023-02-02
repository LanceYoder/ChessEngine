from conversions import *
from piece_maps import *

def evalPos(board):
    print("______________________")
    #white is going, so board.turn=False
    evaluation = 0

    if board.is_checkmate():
        evaluation += 1000

    if board.turn:  # if black is going (so now it is white's "turn"), invert check scores
        evaluation *= -1


    pieces = board.piece_map()

    for p in pieces:
        piece_type = str(pieces[p])
        evaluation += pieceToScore(piece_type)
        print("piecetype: ", piece_type, "square: ", p)
        evaluation += pms(piece_type, p)

    return evaluation * -1
