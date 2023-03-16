from eval import *

# quiesence should maybe be phase dependent:
# opening and ending, check ALL captures
# middle game, check only same square captures
# check checks for both? to what depth?
def quiescence(board, depth, lowest, highest, colorWhite):
    #print("QQQQQQQ 1 - ", depth)
    print("depthMax: ", depth)
    if depth == 0:
        #print("end quie")
        return evalPos(board, colorWhite)
    moves = board.legal_moves
    minEval = float("-inf")
    lo = lowest
    hi = highest

    for i, move in enumerate(moves):
        #print("Qmove    ", move)
        if not board.is_capture(move):
            #print("-------------")
            continue
        # print("moveMax ", move, "color: ", board.turn)
        board.push(move)
        if board.is_game_over():
            # print("BOARD.GAME_OVER")
            evaluation = evalPos(board, colorWhite)
            board.pop()
            return evaluation

        evaluation = QmoveSearchMin(board, depth - 1, lo, hi, colorWhite)#, quie)
        board.pop()

        # print("minEvaluation: ", evaluation)
        # print("minEval: ", minEval)
        if evaluation > minEval:
            minEval = evaluation

        if minEval >= hi:
            return minEval
        lo = max(lo, minEval)

    return minEval

def QmoveSearchMin(board, depth, lowest, highest, colorWhite):
    #print("QQQQQQQ 2 - ", depth)
    print("depthMin: ", depth)
    if depth == 0:
        #print("end q min move")
        return evalPos(board, colorWhite)
    #print("lk")
    moves = board.legal_moves
    maxEval = float("inf")
    lo = lowest
    hi = highest

    for i, move in enumerate(moves):
        #print("Qmove    ", move)
        if not board.is_capture(move):
            #print("-------------")
            continue
        #else:
        #    print(str(move))
        # print("moveMin: ", move, "color: ", board.turn)
        board.push(move)
        if board.is_game_over():
            evaluation = evalPos(board, colorWhite)
            board.pop()
            return evaluation

        evaluation = quiescence(board, depth - 1, lo, hi, colorWhite)
        board.pop()
        # print("maxEvaluation: ", evaluation)
        # print("maxEval: ", maxEval)
        if maxEval > evaluation:
            maxEval = evaluation

        if maxEval <= lo:
            return maxEval
        hi = min(hi, maxEval)

    return maxEval