from eval import *

def qMax(board, depth, alpha, beta, colorWhite, gamephase, set1, set2):
    if depth == 0:
        return evalPos(board, colorWhite, gamephase, set1, set2)
    moves = board.legal_moves
    minEval = float("-inf")

    for i, move in enumerate(moves):
        if not board.is_check():
            continue

        board.push(move)
        if board.is_game_over():
            evaluation = evalPos(board, colorWhite,
                                 gamephase, set1, set2)
            board.pop()
            return evaluation

        evaluation = qMin(board, depth - 1, alpha, beta,
                          colorWhite, gamephase, set1, set2)
        board.pop()

        minEval = max(evaluation, minEval)

        if minEval >= beta:
            return minEval
        alpha = max(alpha, minEval)

    return minEval

def qMin(board, depth, alpha, beta, colorWhite, gamephase, set1, set2):

    if depth == 0:
        return evalPos(board, colorWhite, gamephase, set1, set2)

    moves = board.legal_moves
    maxEval = float("inf")

    for i, move in enumerate(moves):
        if not board.is_check():
            continue

        board.push(move)
        if board.is_game_over():
            evaluation = evalPos(board, colorWhite,
                                 gamephase, set1, set2)
            board.pop()
            return evaluation

        evaluation = qMax(board, depth - 1, alpha, beta,
                          colorWhite, gamephase, set1, set2)
        board.pop()

        maxEval = min(evaluation, maxEval)

        if maxEval <= alpha:
            return maxEval
        beta = min(beta, maxEval)

    return maxEval