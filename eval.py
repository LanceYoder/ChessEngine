import chess
import numpy as np

from utilities import pieceToScore
from piece_maps import pms

def evalPos(board, colorWhite, gamephase):
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
    #this might be wrong
    if len(board.pieces(chess.BISHOP, not board.turn)) == 2:
        evaluation += 50

    pieces = board.piece_map()
    for p in pieces:
        piece_type = str(pieces[p])
        # piece weights
        evaluation += pieceToScore(piece_type)
        # piece-square evaluation
        evaluation += pms(piece_type, p, gamephase)
    #print(str(evaluation))

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

    queens = len(board.pieces(chess.QUEEN, chess.WHITE)) + len(board.pieces(chess.QUEEN, chess.BLACK))
    rooks = len(board.pieces(chess.ROOK, chess.WHITE)) + len(board.pieces(chess.ROOK, chess.BLACK))
    bishops = len(board.pieces(chess.BISHOP, chess.WHITE)) + len(board.pieces(chess.BISHOP, chess.BLACK))
    knights = len(board.pieces(chess.KNIGHT, chess.WHITE)) + len(board.pieces(chess.KNIGHT, chess.BLACK))
    minors = rooks + bishops + knights
    pawns = len(board.pieces(chess.PAWN, chess.WHITE)) + len(board.pieces(chess.PAWN, chess.BLACK))

    gamePhase += (2 - queens) * 12
    gamePhase += (12 - minors) * 4
    gamePhase += (16 - pawns)

    gamePhase += board.fullmove_number / 2

    return gamePhase
