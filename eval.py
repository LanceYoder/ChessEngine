from conversions import *
from piece_maps import *

def evalPos(board):
    #white is going, so board.turn=False
    evaluation = 0

    if board.is_checkmate():
        evaluation += 1000

    if board.turn:  # if black is going (so now it is white's "turn"), invert check scores
        evaluation *= -1


    #pieces = board.piece_map()

    #for p in pieces:
    #    piece_type = pieces[p]
    #    sc = pieceToScore(piece_type)
    #    evaluation += sc
    #    evaluation += pms(pieces[p], p)

    fen = board.fen()
    for c in fen.split(" ")[0]:
        if c.isalpha():
            sc = pieceToScore(c)
            evaluation += sc

    # print("EVAL: ", evaluation)

    return evaluation * -1
