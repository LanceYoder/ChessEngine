from quiescence import *
from utilities import make_PV
import globs
from globs import trad

def moveSearchMax(board, cur_level, depth, alpha, beta, colorWhite,
                  gamePhase, PV, searchPV, set1=trad, set2=trad):

    if cur_level == 0 or board.is_game_over() or board.is_stalemate():
        return evalPos(board, colorWhite, gamePhase, set1, set2), PV

    moves = board.legal_moves
    minEval = float("-inf")

    # try pv
    move = PV[depth - cur_level][0]
    if move is not None and searchPV and board.is_legal(move):

        board.push(move)

        if board.is_checkmate():
            if board.turn:
                evaluation = -1000000 - cur_level if colorWhite \
                    else 1000000 + cur_level
            else:
                evaluation = 1000000 + cur_level if colorWhite \
                    else -1000000 - cur_level

        else:
            evaluation, PV = moveSearchMin(
                board, cur_level - 1, depth, alpha, beta,
                colorWhite, gamePhase, PV, True, set1=set1, set2=set2)

        board.pop()

        minEval = max(evaluation, minEval)

        if minEval >= beta:
            return minEval, PV

        alpha = max(minEval, alpha)

        if alpha > PV[depth - cur_level][1]:
            if 1 == cur_level:
                PV = make_PV(globs.pvLength)
            PV[depth - cur_level] = (move, alpha)

    for move in moves:

        board.push(move)
        if board.is_checkmate():
            if board.turn:
                evaluation = -1000000 - cur_level if colorWhite \
                    else 1000000 + cur_level
            else:
                evaluation = 1000000 + cur_level if colorWhite \
                    else -1000000 - cur_level

        else:
            evaluation, PV = moveSearchMin(
                board, cur_level - 1, depth, alpha, beta,
                colorWhite, gamePhase, PV, False, set1=set1, set2=set2)

        board.pop()

        minEval = max(evaluation, minEval)

        if minEval >= beta:
            return minEval, PV

        alpha = max(minEval, alpha)

        if alpha > PV[depth - cur_level][1]:
            if 1 == cur_level:
                PV = make_PV(globs.pvLength)
            PV[depth - cur_level] = (move, alpha)

    return minEval, PV

def moveSearchMin(board, cur_level, depth, alpha, beta,  colorWhite,
                  gamePhase, PV, searchPV, set1=trad, set2=trad):

    if cur_level == 0 or board.is_game_over() or board.is_stalemate():
        return evalPos(board, colorWhite, gamePhase, set1, set2), PV

    moves = board.legal_moves
    maxEval = float("inf")

    # try PV
    move = PV[depth - cur_level][0]
    if move is not None and searchPV and board.is_legal(move):

        board.push(move)

        if board.is_checkmate():
            if board.turn:
                evaluation = -1000000 - cur_level if colorWhite \
                    else 1000000 + cur_level
            else:
                evaluation = 1000000 + cur_level if colorWhite \
                    else -1000000 - cur_level

        else:
            evaluation, PV = moveSearchMax(
                board, cur_level - 1, depth, alpha, beta,
                colorWhite, gamePhase, PV, True, set1=set1, set2=set2)
        board.pop()

        maxEval = min(evaluation, maxEval)

        if maxEval <= alpha:
            return maxEval, PV

        beta = min(maxEval, beta)

        if beta < PV[depth - cur_level][1]:
            if 1 == cur_level:
                PV = make_PV(globs.pvLength)
            PV[depth - cur_level] = (move, beta)

    for move in moves:

        board.push(move)

        if board.is_checkmate():
            if board.turn:
                evaluation = -1000000 - cur_level if colorWhite \
                    else 1000000 + cur_level
            else:
                evaluation = 1000000 + cur_level if colorWhite \
                    else -1000000 - cur_level

        else:
            evaluation, PV = moveSearchMax(
                board, cur_level - 1, depth, alpha, beta,
                colorWhite, gamePhase, PV, False, set1=set1, set2=set2)
        board.pop()

        maxEval = min(evaluation, maxEval)

        if maxEval <= alpha:
            return maxEval, PV

        beta = min(maxEval, beta)

        if beta < PV[depth - cur_level][1]:
            if 1 == cur_level:
                PV = make_PV(globs.pvLength)
            PV[depth - cur_level] = (move, beta)

    return maxEval, PV
