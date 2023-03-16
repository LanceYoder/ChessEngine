from quiescence import *
import globs

def moveSearchMax(board, cur_level, depth, lowest, highest, colorWhite):
    #rint("okokokMAX: ", depth)
    if cur_level == 0:
        #print("end msMax+++++++")
        e_val = evalPos(board, colorWhite)
        #quie = quiescence(board, 2, lowest, highest, colorWhite)
        return (e_val, None)# if e_val > quie else (quie, None)
    moves = board.legal_moves
    minEval = float("-inf")
    lo = lowest
    hi = highest
    bestMove = None

    for i, move in enumerate(moves):
        #print("Smove    ", move)
        board.push(move)
        if board.is_game_over():
            evaluation = evalPos(board,colorWhite)
            bestMove = move
            board.pop()
            return evaluation, bestMove

        evaluation, _ = moveSearchMin(board, cur_level - 1, depth, lo, hi, colorWhite)
        board.pop()

        if minEval < evaluation:
            minEval = evaluation
            bestMove = move

        if minEval >= hi:
            #if depth > len(globs.PV):
            #    globs.PV.append(bestMove)
            #else:
            #    globs.PV[(depth - cur_level)/2] = bestMove
            return minEval, bestMove
        lo = max(lo, minEval)



    return minEval, bestMove

def moveSearchMin(board, cur_level, depth, lowest, highest, colorWhite):
    #print("okokokMIN: ", depth)
    if cur_level == 0:
        #print("end moveMin-------")
        e_val = evalPos(board, colorWhite)
        #quie = QmoveSearchMin(board, 2, lowest, highest, colorWhite)
        return (e_val, None)# if e_val < quie else (quie, None)
    moves = board.legal_moves
    maxEval = float("inf")
    lo = lowest
    hi = highest
    bestMove = None

    for i, move in enumerate(moves):
        #print("Smove    ", move)
        board.push(move)
        if board.is_game_over():
            evaluation = evalPos(board, colorWhite)
            bestMove = move
            board.pop()
            return evaluation, bestMove

        evaluation, _ = moveSearchMax(board, cur_level - 1, depth, lo, hi, colorWhite)
        board.pop()

        if maxEval > evaluation:
            maxEval = evaluation
            bestMove = move

        if maxEval <= lo:
            return maxEval, bestMove
        hi = min(hi, maxEval)

    return maxEval, bestMove
