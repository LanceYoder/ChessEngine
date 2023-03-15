from eval import *

# quiesence should maybe be phase dependent:
# opening and ending, check ALL captures
# middle game, check only same square captures
# check checks for both? to what depth?
def quiescence(board, depth, lowest, highest):
    #print("QQQQQQQ 1 - ", depth)
    print("depthMax: ", depth)
    if depth == 0:
        #print("end quie")
        return evalPos(board), None
    moves = board.legal_moves
    minEval = float("-inf")
    lo = lowest
    hi = highest
    bestMove = None

    for i, move in enumerate(moves):
        #print("Qmove    ", move)
        if not board.is_capture(move):
            #print("-------------")
            continue
        # print("moveMax ", move, "color: ", board.turn)
        board.push(move)
        if board.is_game_over():
            # print("BOARD.GAME_OVER")
            evaluation = evalPos(board)
            bestMove = move
            board.pop()
            return evaluation, bestMove

        evaluation, _ = QmoveSearchMin(board, depth - 1, lo, hi)#, quie)
        board.pop()

        # print("minEvaluation: ", evaluation)
        # print("minEval: ", minEval)
        if evaluation > minEval:
            minEval = evaluation
            bestMove = move

        if minEval >= hi:
            return minEval, bestMove
        lo = max(lo, minEval)

    return minEval, bestMove

def QmoveSearchMin(board, depth, lowest, highest):
    #print("QQQQQQQ 2 - ", depth)
    print("depthMin: ", depth)
    if depth == 0:
        #print("end q min move")
        return evalPos(board), None
    #print("lk")
    moves = board.legal_moves
    maxEval = float("inf")
    lo = lowest
    hi = highest
    bestMove = None

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
            evaluation = evalPos(board)
            bestMove = move
            board.pop()
            return evaluation, bestMove

        evaluation, _ = quiescence(board, depth - 1, lo, hi)
        board.pop()
        # print("maxEvaluation: ", evaluation)
        # print("maxEval: ", maxEval)
        if maxEval > evaluation:
            maxEval = evaluation
            bestMove = move

        if maxEval <= lo:
            return maxEval, move
        hi = min(hi, maxEval)

    return maxEval, bestMove