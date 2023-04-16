from quiescence import *
from utilities import make_PV
import globs

def moveSearchMax(board, cur_level, depth, lowest, highest, colorWhite, gamephase, PV, searchPV):

    if cur_level == 0 or board.is_game_over() or board.is_stalemate():
        return evalPos(board, colorWhite, gamephase), PV

    moves = board.legal_moves
    minEval = float("-inf")
    lo = lowest
    hi = highest

    # try pv
    move = PV[depth - cur_level][0]
    if move is not None and searchPV and board.is_legal(move):

        board.push(move)

        evaluation, PV = moveSearchMin(board, cur_level - 1, depth, lo, hi, colorWhite, gamephase, PV, True)
        board.pop()

        minEval = max(evaluation, minEval)

        if minEval >= hi:
            return minEval, PV

        lo = max(minEval, lo)

        if lo > PV[depth - cur_level][1]:
            if 1 == cur_level:
                PV = make_PV(globs.pvLength)
            PV[depth - cur_level] = (move, lo)

    for move in moves:
        board.push(move)
        evaluation, PV = moveSearchMin(board, cur_level - 1, depth, lo, hi, colorWhite, gamephase, PV, False)
        board.pop()

        minEval = max(evaluation, minEval)

        if minEval >= hi:
            return minEval, PV

        lo = max(minEval, lo)

        if lo > PV[depth - cur_level][1]:
            if 1 == cur_level:
                PV = make_PV(globs.pvLength)
            PV[depth - cur_level] = (move, lo)

    return minEval, PV

def moveSearchMin(board, cur_level, depth, lowest, highest, colorWhite, gamephase, PV, searchPV):

    if cur_level == 0 or board.is_game_over() or board.is_stalemate():
        return evalPos(board, colorWhite, gamephase), PV

    moves = board.legal_moves
    maxEval = float("inf")
    lo = lowest
    hi = highest

    # try PV
    move = PV[depth - cur_level][0]
    if move is not None and searchPV and board.is_legal(move):

        board.push(move)

        evaluation, PV = moveSearchMax(board, cur_level - 1, depth, lo, hi, colorWhite, gamephase, PV, True)
        board.pop()

        maxEval = min(evaluation, maxEval)

        if maxEval <= lo:
            return maxEval, PV

        hi = min(maxEval, hi)

        if hi < PV[depth - cur_level][1]:
            if 1 == cur_level:
                PV = make_PV(globs.pvLength)
            PV[depth - cur_level] = (move, hi)

    for move in moves:

        board.push(move)

        evaluation, PV = moveSearchMax(board, cur_level - 1, depth, lo, hi, colorWhite, gamephase, PV, False)
        board.pop()

        maxEval = min(evaluation, maxEval)

        if maxEval <= lo:
            return maxEval, PV

        hi = min(maxEval, hi)

        if hi < PV[depth - cur_level][1]:
            if 1 == cur_level:
                PV = make_PV(globs.pvLength)
            PV[depth - cur_level] = (move, hi)

    return maxEval, PV
