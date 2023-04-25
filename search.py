from quiescence import *
from utilities import make_PV
import globs
from globs import traditional

def moveSearchMax(board, cur_level, depth, lowest, highest, colorWhite, gamephase, PV, searchPV, set1=traditional, set2=traditional):

    if cur_level == 0 or board.is_game_over() or board.is_stalemate():
        return evalPos(board, colorWhite, gamephase, set1, set2), PV

    moves = board.legal_moves
    minEval = float("-inf")
    lo = lowest
    hi = highest
    bestMove = None

    # try pv
    #move = PV[depth - cur_level][0]
    if False:#move is not None and searchPV and board.is_legal(move):

        board.push(move)

        if board.is_checkmate():
            if board.turn:
                evaluation = -1000000 - cur_level if colorWhite else 1000000 + cur_level
            else:
                evaluation = 1000000 + cur_level if colorWhite else -1000000 - cur_level

        else:
            evaluation, PV = moveSearchMin(board, cur_level - 1, depth, lo, hi, colorWhite, gamephase, PV, True, set1=set1, set2=set2)

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
        if board.is_checkmate():
            if board.turn:
                evaluation = -1000000 - cur_level if colorWhite else 1000000 + cur_level
            else:
                evaluation = 1000000 + cur_level if colorWhite else -1000000 - cur_level

        else:
            evaluation, PV = moveSearchMin(board, cur_level - 1, depth, lo, hi, colorWhite, gamephase, PV, False, set1=set1, set2=set2)

        board.pop()

        #minEval = max(evaluation, minEval)
        if evaluation > minEval:
            minEval = evaluation
            bestMove = move

        #if minEval >= hi:
        #    return minEval, PV

        #lo = max(minEval, lo)

        #if lo > PV[depth - cur_level][1]:
        #    if 1 == cur_level:
        #        PV = make_PV(globs.pvLength)
        #    PV[depth - cur_level] = (move, lo)

    return minEval, bestMove#PV

def moveSearchMin(board, cur_level, depth, lowest, highest, colorWhite, gamephase, PV, searchPV, set1=traditional, set2=traditional):

    if cur_level == 0 or board.is_game_over() or board.is_stalemate():
        return evalPos(board, colorWhite, gamephase, set1, set2), PV

    moves = board.legal_moves
    maxEval = float("inf")
    lo = lowest
    hi = highest
    bestMove = None

    # try PV
    #move = PV[depth - cur_level][0]
    if False:#move is not None and searchPV and board.is_legal(move):

        board.push(move)

        if board.is_checkmate():
            if board.turn:
                evaluation = -1000000 - cur_level if colorWhite else 1000000 + cur_level
            else:
                evaluation = 1000000 + cur_level if colorWhite else -1000000 - cur_level

        else:
            evaluation, PV = moveSearchMax(board, cur_level - 1, depth, lo, hi, colorWhite, gamephase, PV, True, set1=set1, set2=set2)
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

        if board.is_checkmate():
            if board.turn:
                evaluation = -1000000 - cur_level if colorWhite else 1000000 + cur_level
            else:
                evaluation = 1000000 + cur_level if colorWhite else -1000000 - cur_level

        else:
            evaluation, PV = moveSearchMax(board, cur_level - 1, depth, lo, hi, colorWhite, gamephase, PV, False, set1=set1, set2=set2)
        board.pop()

        #maxEval = min(evaluation, maxEval)
        if evaluation < maxEval:
            maxEval = evaluation
            bestMove = move

        #if maxEval <= lo:
        #    return maxEval, PV

        #hi = min(maxEval, hi)

        #if hi < PV[depth - cur_level][1]:
        #    if 1 == cur_level:
        #        PV = make_PV(globs.pvLength)
        #    PV[depth - cur_level] = (move, hi)

    return maxEval, bestMove#PV
