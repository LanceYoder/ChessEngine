from quiescence import *
import globs

def moveSearchMax(board, cur_level, depth, lowest, highest, colorWhite, gamephase, PV, searchPV):
    #bfen = board.fen().split(' ')[0]
    # print("okokokMAX: ", depth)
    if cur_level == 0:
        # print("end moveMin-------")
        #e_val, _ = globs.TT.get(bfen, (None, None))
        #if not e_val:
        e_val = evalPos(board, colorWhite, gamephase)
        #    globs.TT[bfen] = (e_val, depth)
        #quie = quiescence(board, 2, lowest, highest, colorWhite)
        # for quiescence, check if previous move was a capture, if it was look for captures on the same square?
        return e_val, None, PV# if e_val > quie else (quie, None)

    moves = board.legal_moves
    minEval = float("-inf")
    lo = lowest
    hi = highest
    bestMove = None

    # try PV
    move = PV[depth - cur_level][0]
    if move is not None and searchPV:
        board.push(move)
        if board.is_game_over():
            evaluation = evalPos(board, colorWhite, gamephase)
            bestMove = move
            board.pop()
            return evaluation, bestMove, PV

        evaluation, _, PV = moveSearchMin(board, cur_level - 1, depth, lo, hi, colorWhite, gamephase, PV, True)
        board.pop()

        if evaluation > minEval:
            minEval = evaluation
            bestMove = move

        if minEval >= hi:
            return minEval, bestMove, PV

        if minEval > lo:
            # print(minEval, lo, "  +_+_+_+_+_", cur_level)
            lo = minEval
            if lo > PV[depth - cur_level][1]:
                PV = [(None, float("-inf")), (None, float("inf")), (None, float("-inf")), (None, float("inf")),
                      (None, float("-inf")), (None, float("inf")), (None, float("-inf")), (None, float("inf"))]
                PV[depth - cur_level] = (bestMove, lo)
                print("pvPV level:", depth - cur_level, PV)

    for move in moves:
        #print("Smove    ", move)
        board.push(move)
        if board.is_game_over():
            evaluation = evalPos(board, colorWhite, gamephase)
            bestMove = move
            board.pop()
            return evaluation, bestMove, PV

        evaluation, _, PV = moveSearchMin(board, cur_level - 1, depth, lo, hi, colorWhite, gamephase, PV, False)
        board.pop()

        if evaluation > minEval:
            minEval = evaluation
            bestMove = move

        if minEval >= hi:
            return minEval, bestMove, PV

        if minEval > lo:
            #print(minEval, lo, "  +_+_+_+_+_", cur_level)
            lo = minEval
            if lo > PV[depth - cur_level][1]:
                PV = [(None, float("-inf")), (None, float("inf")), (None, float("-inf")), (None, float("inf")),
                      (None, float("-inf")), (None, float("inf")), (None, float("-inf")), (None, float("inf"))]
                PV[depth - cur_level] = (bestMove, lo)
                print("PV level:", depth - cur_level, PV)
        #print("***********", lo, cur_level)
    #print("---------------", cur_level)

    return minEval, bestMove, PV

def moveSearchMin(board, cur_level, depth, lowest, highest, colorWhite, gamephase, PV, searchPV):
    #bfen = board.fen().split(' ')[0]
    #print("okokokMIN: ", depth)
    if cur_level == 0:
        #print("end moveMin-------")
        #e_val, _ = globs.TT.get(bfen, (None, None))
        #if not e_val:
        e_val = evalPos(board, colorWhite, gamephase)
        #    globs.TT[bfen] = (e_val, depth)
        #quie = QmoveSearchMin(board, 2, lowest, highest, colorWhite)
        # for quiescence, check if previous move was a capture, if it was look for captures on the same square?
        return e_val, None, PV# if e_val < quie else (quie, None)

    moves = board.legal_moves
    maxEval = float("inf")
    lo = lowest
    hi = highest
    bestMove = None

    # try PV
    move = PV[depth - cur_level][0]
    if move is not None and searchPV:
        board.push(move)
        if board.is_game_over():
            evaluation = evalPos(board, colorWhite, gamephase)
            bestMove = move
            board.pop()
            return evaluation, bestMove, PV

        evaluation, _, PV = moveSearchMax(board, cur_level - 1, depth, lo, hi, colorWhite, gamephase, PV, True)
        board.pop()

        if evaluation < maxEval:
            maxEval = evaluation
            bestMove = move

        if maxEval <= lo:
            return maxEval, bestMove, PV

        if maxEval < hi:
            hi = maxEval
            if hi < PV[depth - cur_level][1]:
                PV = [(None, float("-inf")), (None, float("inf")), (None, float("-inf")), (None, float("inf")),
                      (None, float("-inf")), (None, float("inf")), (None, float("-inf")), (None, float("inf"))]
                PV[depth - cur_level] = (bestMove, hi)
                print("pvPV level:", depth - cur_level, PV)

    for move in moves:
        #print("Smove    ", move)
        board.push(move)
        if board.is_game_over():
            evaluation = evalPos(board, colorWhite, gamephase)
            bestMove = move
            board.pop()
            return evaluation, bestMove, PV

        evaluation, _, PV = moveSearchMax(board, cur_level - 1, depth, lo, hi, colorWhite, gamephase, PV, False)
        board.pop()

        if evaluation < maxEval:
            maxEval = evaluation
            bestMove = move

        if maxEval <= lo:
            return maxEval, bestMove, PV

        if maxEval < hi:
            hi = maxEval
            if hi < PV[depth - cur_level][1]:
                PV = [(None, float("-inf")), (None, float("inf")), (None, float("-inf")), (None, float("inf")),
                      (None, float("-inf")), (None, float("inf")), (None, float("-inf")), (None, float("inf"))]
                PV[depth - cur_level] = (bestMove, hi)
                print("PV level:", depth - cur_level, PV)

    return maxEval, bestMove, PV
