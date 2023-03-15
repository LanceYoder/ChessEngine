from eval import *
from quiescence import *

# board is the current board, depth is the number of levels yet to recurse
def moveSearchMax(board, depth, lowest, highest):
    #rint("okokokMAX: ", depth)
    if depth == 0:
        #print("end msMax+++++++")
        e_val = evalPos(board)
        #quie, _ = quiescence(board, 2, lowest, highest)
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
            evaluation = evalPos(board)
            bestMove = move
            board.pop()
            return evaluation, bestMove

        evaluation, _ = moveSearchMax(board, depth - 1, hi, lo)
        board.pop()

        if minEval < evaluation:
            minEval = evaluation
            bestMove = move

        if minEval >= hi:
            return minEval, bestMove
        lo = max(lo, minEval)

    return minEval, bestMove

def moveSearchMin(board, depth, lowest, highest):
    #print("okokokMIN: ", depth)
    if depth == 0:
        #print("end moveMin-------")
        e_val = evalPos(board)
        #quie, _ = quiescence(board, 2, lowest, highest)
        return (e_val, None)# if e_val > quie else (quie, None)
    moves = board.legal_moves
    maxEval = float("inf")
    lo = lowest
    hi = highest
    bestMove = None

    for i, move in enumerate(moves):
        #print("Smove    ", move)
        board.push(move)
        if board.is_game_over():
            evaluation = evalPos(board)
            bestMove = move
            board.pop()
            return evaluation, bestMove

        evaluation, _ = moveSearchMax(board, depth - 1, lo, hi)
        board.pop()

        if maxEval > evaluation:
            maxEval = evaluation
            bestMove = move

        if maxEval <= lo:
            return maxEval, move
        hi = min(hi, maxEval)

    return maxEval, bestMove
