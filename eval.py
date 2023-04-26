import chess
import numpy as np
from piece_maps import pst
from globs import trad, mich, kauf, fruit, alpha
import timeit





def evalPos(board, colorWhite, gamephase, set1, set2):

    evaluation = 0

    # randomization so it doesn't just play rook moves when stuck
    # this shouldn't be necessary if my eval is good
    # but it might help make things interesting
    evaluation += np.random.rand() * 2 - 1

    # mobility
    evaluation -= board.legal_moves.count() / 6

    # bishop pair
    if len(board.pieces(chess.BISHOP, not board.turn)) == 2:
        evaluation += 50

    pieces = board.piece_map()
    for sqr in pieces:
        piece_type = str(pieces[sqr])
        # piece weights
        evaluation += trad[piece_type]
        #if piece_type.isupper():
        #    evaluation += set1[piece_type]
        #else:
        #    evaluation += set2[piece_type]
        # piece-square evaluation
        evaluation += pst(piece_type, sqr, gamephase)

    if board.is_stalemate():
        if evaluation > 0 ^ colorWhite:
            return 1000
        else:
            return -1000

    return evaluation if colorWhite else -1 * evaluation

# return an int indicating game phase
# 0-100, 0 being opening, 100 being endgame
def game_phase(board):
    gamePhase = 0
    pieces = board.piece_map()
    gamePhase += (32 - len(pieces)) * 3

    if not board.has_castling_rights(chess.WHITE):
        gamePhase += 5
    if not board.has_castling_rights(chess.BLACK):
        gamePhase += 5

    queens = len(board.pieces(chess.QUEEN, chess.WHITE)) + \
             len(board.pieces(chess.QUEEN, chess.BLACK))
    rooks = len(board.pieces(chess.ROOK, chess.WHITE)) + \
            len(board.pieces(chess.ROOK, chess.BLACK))
    bishops = len(board.pieces(chess.BISHOP, chess.WHITE)) + \
              len(board.pieces(chess.BISHOP, chess.BLACK))
    knights = len(board.pieces(chess.KNIGHT, chess.WHITE)) + \
              len(board.pieces(chess.KNIGHT, chess.BLACK))
    minors = rooks + bishops + knights
    pawns = len(board.pieces(chess.PAWN, chess.WHITE)) + \
            len(board.pieces(chess.PAWN, chess.BLACK))

    gamePhase += (2 - queens) * 12
    gamePhase += (12 - minors) * 4
    gamePhase += (16 - pawns)

    gamePhase += board.fullmove_number / 2

    return gamePhase if gamePhase < 100 else 100

#board = chess.Board()
#board.push(chess.Move.from_uci('d2d4'))
#board.push(chess.Move.from_uci('d7d5'))
#board.push(chess.Move.from_uci('e2e4'))
#print(timeit.timeit('evalPos(board, True, 15)', globals=globals(), number=10000))