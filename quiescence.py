from eval import *

# quiesence should maybe be phase dependent:
# opening and ending, check ALL captures
# middle game, check only same square captures
# check checks for both? to what depth?
def quiescenceMax(board, depth, lowest, highest, colorWhite, gamephase):
    if depth == 0:
        return evalPos(board, colorWhite, gamephase)
    moves = board.legal_moves
    minEval = float("-inf")
    lo = lowest
    hi = highest

    for i, move in enumerate(moves):
        if not board.is_check():
            continue

        board.push(move)
        if board.is_game_over():
            evaluation = evalPos(board, colorWhite, gamephase)
            board.pop()
            return evaluation

        evaluation = quiescenceMin(board, depth - 1, lo, hi, colorWhite, gamephase)
        board.pop()

        minEval = max(evaluation, minEval)

        if minEval >= hi:
            return minEval
        lo = max(lo, minEval)

    return minEval

def quiescenceMin(board, depth, lowest, highest, colorWhite, gamephase):

    if depth == 0:
        return evalPos(board, colorWhite, gamephase)

    moves = board.legal_moves
    maxEval = float("inf")
    lo = lowest
    hi = highest

    for i, move in enumerate(moves):
        if not board.is_check():
            continue

        board.push(move)
        if board.is_game_over():
            evaluation = evalPos(board, colorWhite, gamephase)
            board.pop()
            return evaluation

        evaluation = quiescenceMax(board, depth - 1, lo, hi, colorWhite, gamephase)
        board.pop()

        maxEval = min(evaluation, maxEval)

        if maxEval <= lo:
            return maxEval
        hi = min(hi, maxEval)

    return maxEval