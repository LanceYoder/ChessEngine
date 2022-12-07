from eval import *

# board is the current board, depth is the number of levels yet to recurse
def moveSearchMax(board, depth, lowest, highest):
    print("depthmax: ", depth)
    if depth == 0:
        return evalPos(board), None
    moves = board.legal_moves
    minEval = float("-inf")
    lo = lowest
    hi = highest
    bestMove = None

    for i, move in enumerate(moves):

        print("moveMax ", move, "color: ", board.turn)
        board.push(move)
        if board.is_game_over():
            print("BOARD GAME OVER")
            evaluation = evalPos(board)
            bestMove = move
            board.pop()
            return evaluation, bestMove

        evaluation, _ = moveSearchMin(board, depth - 1, lo, hi)
        board.pop()

        print("minEvaluation: ", evaluation)
        print("minEval: ", minEval)
        if evaluation > minEval:
            minEval = evaluation
            bestMove = move

        if minEval >= hi:
            return minEval, bestMove
        lo = max(lo, minEval)

    return minEval, bestMove

def moveSearchMin(board, depth, lowest, highest):
    print("depthmin: ", depth)
    if depth == 0:
        return evalPos(board), None
    moves = board.legal_moves
    maxEval = float("inf")
    lo = lowest
    hi = highest
    bestMove = None

    for i, move in enumerate(moves):
        print("moveMin: ", move, "color: ", board.turn)
        board.push(move)
        if board.is_game_over():
            evaluation = evalPos(board)
            bestMove = move
            board.pop()
            return evaluation, bestMove

        evaluation, _ = moveSearchMax(board, depth - 1, lo, hi)
        board.pop()
        print("maxEvaluation: ", evaluation)
        print("maxEval: ", maxEval)
        if maxEval > evaluation:
            maxEval = evaluation
            bestMove = move

        if maxEval <= lo:
            return maxEval, move
        hi = min(hi, maxEval)

    return maxEval, bestMove
