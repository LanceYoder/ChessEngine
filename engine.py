#!/usr/bin/env python

#-----------------------------------------------------------------------
# engine.py
# Author: Lance Yoder
#-----------------------------------------------------------------------

import chess
import numpy as np
import time
import argparse

import sys, codecs

if sys.stdout.encoding is None or sys.stdout.encoding == 'ANSI_X3.4-1968':
    utf8_writer = codecs.getwriter('UTF-8')
    if sys.version_info.major < 3:
        sys.stdout = utf8_writer(sys.stdout, errors='replace')
    else:
        sys.stdout = utf8_writer(sys.stdout.buffer, errors='replace')

def charToUni(c):
    if c == 'P':
        return u'\N{WHITE CHESS PAWN}'
    if c == 'R':
        return u'\N{WHITE CHESS ROOK}'
    if c == 'N':
        return u'\N{WHITE CHESS KNIGHT}'
    if c == 'B':
        return u'\N{WHITE CHESS BISHOP}'
    if c == 'Q':
        return u'\N{WHITE CHESS QUEEN}'
    if c == 'K':
        return u'\N{WHITE CHESS KING}'
    if c == 'p':
        return u'\N{BLACK CHESS PAWN}'
    if c == 'r':
        return u'\N{BLACK CHESS ROOK}'
    if c == 'n':
        return u'\N{BLACK CHESS KNIGHT}'
    if c == 'b':
        return u'\N{BLACK CHESS BISHOP}'
    if c == 'q':
        return u'\N{BLACK CHESS QUEEN}'
    if c == 'k':
        return u'\N{BLACK CHESS KING}'

def pieceToScore(c):
    if c == 'P':  # caps are white
        return 1
    if c == 'R':
        return 5
    if c == 'N':
        return 3
    if c == 'B':
        return 3
    if c == 'Q':
        return 9
    if c == 'K':
        return 100
    if c == 'p':  # lowercase is black
        return -1
    if c == 'r':
        return -5
    if c == 'n':
        return -3
    if c == 'b':
        return -3
    if c == 'q':
        return -9
    if c == 'k':
        return -100
    print("c: ", c)
    return 1000

def printfen(fen):
    rows = fen.split('/')
    j = 0
    for row in rows:
        print(f'{8 - j} ', end='')
        j += 1
        for c in row:
            if c.isalpha():
                print(f'{charToUni(c)}', end=' ')
            else:
                for i in range(int(c)):
                    print('.', end=' ')
        print()
    print('  a b c d e f g h')



def mainTerminal():

    board = chess.Board()

    boardfen = board.fen().split(' ', 1)[0]

    printfen(boardfen)
    print("------------------")

    while not board.is_game_over():
        try:
            INPUT = input("Move:\n")

            move = chess.Move.from_uci(INPUT)
            while move not in board.legal_moves:
                INPUT = input("Not a legal move. Try again:\n")
                print("input: ", INPUT)
                move = chess.Move.from_uci(INPUT)

            board.push(move)

            if board.is_game_over():
                continue

            # black should want a very negative score, white a very positive score

            _, damove = moveSearchMax(board, 5, float("-inf"), float("inf"))

            print("Opponent's move: ", damove)

            board.push(damove)

            boardfen = board.fen().split(' ', 1)[0]

            printfen(boardfen)
            #print("------------------")
        except Exception as ex:
            print("oopss, ", ex)

    boardfen = board.fen().split(' ', 1)[0]
    printfen(boardfen)
    if board.outcome().winner:
        print("White wins")
    else:
        print("Black wins")


def setup():
    board = chess.Board()

    boardfen = board.fen().split(' ', 1)[0]

    return board, boardfen

def main():
    my_file = open("my_file.txt", "w")
    my_file.write(f'timeeex: {time.time()} \n')
    my_file.write("wrote input?\n")

    board, boardfen = setup()

    sys.stdout.write("feature done=0" + "\n")
    sys.stdout.write("feature reuse=0" + "\n")
    sys.stdout.write("feature done=1" + "\n")
    sys.stdout.flush()

    try:
        processInput(my_file, board, boardfen)
    finally:
        my_file.close()
    return


def processInput(my_file, board, boardfen):
    while True:
        INPUT = "NOPE"
        try:
            INPUT = input()
        except KeyboardInterrupt as ki:
            sys.stdout.write(repr(ki))
            sys.stdout.write(INPUT)
            sys.stdout.flush()

        if INPUT == "":
            break
        #inArray = INPUT.rsplit()
        try:
            move = chess.Move.from_uci(INPUT)

            board.push(move)

            if board.is_game_over():
                continue

            # black should want a very negative score, white a very positive score

            _, damove = moveSearchMax(board, 5, float("-inf"), float("inf"))

            print("da", damove)

            board.push(damove)

            sys.stdout.write("move " + damove.uci() + "\n")
            sys.stdout.flush()
        except Exception as ex:
            sys.stdout.write(repr(ex) + "\n")
            sys.stdout.write(INPUT + "\n")
            sys.stdout.flush()
    return

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


def evalPos(board):
    #white is going, so board.turn=False
    evaluation = 0

    if board.is_checkmate():
        evaluation += 1000

    if board.turn:  # if black is going (so now it is white's "turn"), invert check scores
        evaluation *= -1


    fen = board.fen()
    for c in fen.split(" ")[0]:
        if c.isalpha():
            sc = pieceToScore(c)
            evaluation += sc

    print("EVAL: ", evaluation)

    return evaluation * -1



if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'terminal':
            mainTerminal()
        else:
            print("Usage: python engine.py terminal")
    else:
        main()
