#!/usr/bin/env python

#-----------------------------------------------------------------------
# engine.py
# Author: Lance Yoder
#-----------------------------------------------------------------------

import sys
import codecs
import time
from multiprocessing import Manager, Process

from utilities import *
from search import *
from stocky import *
import globs

#############################
# weird thing to make it work
#############################
if sys.stdout.encoding is None or sys.stdout.encoding == 'ANSI_X3.4-1968':
    utf8_writer = codecs.getwriter('UTF-8')
    if sys.version_info.major < 3:
        sys.stdout = utf8_writer(sys.stdout, errors='replace')
    else:
        sys.stdout = utf8_writer(sys.stdout.buffer, errors='replace')
#############################



def handle_input(board):

    INPUT = input()

    if INPUT == "white":
        print("WHITE WHITE WHITE")
        input()
        globs.colorWhite = True
        return True
    elif INPUT == "black":
        print("BLACK BLACK BLACK")
        globs.colorWhite = False

    try:
        move = chess.Move.from_uci(INPUT)
    except ValueError as ex:
        print(ex)
        return

    board.push(move)
    return True

def processInput(board, depth):

    while True:
        if not handle_input(board):
            continue

        try:
            if board.is_game_over():
                continue

            #if len(board.piece_map()) < 10:
            #    depth = 6

            #for i in range(1, 7, 2):
            _, move = moveSearchMax(board, depth, 1, float("-inf"), float("inf"), globs.colorWhite)

            board.push(move)

            sys.stdout.write("move " + move.uci() + "\n")
            sys.stdout.flush()
        except Exception as ex:
            sys.stdout.write(repr(ex) + "\n")
            sys.stdout.flush()
            raise Exception(repr(ex))
    return

def mainTerminal(board, board_fen, depth):

    print_fen(board_fen)
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
            _, move = moveSearchMax(board, depth, float("-inf"), float("inf"))
            #_, move = quiescence(board, depth, float("-inf"), float("inf"))

            print("Opponent's move: ", move)

            board.push(move)

            board_fen = board.fen().split(' ', 1)[0]

            print_fen(board_fen)
            # print("------------------")
        except Exception as ex:
            print("oops, ", ex)

    board_fen = board.fen().split(' ', 1)[0]
    print_fen(board_fen)
    if board.outcome().winner:
        print("White wins")
    else:
        print("Black wins")

def mainStocky(i, returnDict, depth, t):
    outcomes = np.array([0.0, 0.0])

    for j in range(1):
        board, _ = setup()
        print("Game " + str(j) + " on Thread " + str(i))
        k = 0
        while True:
            print(". Thread " + str(i) + " on Move " + str(k))
            k += 1
            move = takeStock(board, board.fen())

            move = chess.Move.from_uci(move)

            board.push(move)
            #print_fen(board.fen().split(' ', 1)[0])
            #print("_________________")

            if board.is_game_over():
                print("IT'S ALL OVER")
                print(board.outcome().result())
                if board.outcome().winner is None:
                    returnDict.append(np.array([0.5, 0.5]))
                    outcomes += np.array([0.5, 0.5])
                elif board.outcome().winner:
                    returnDict.append(np.array([1, 0]))
                    outcomes += np.array([1, 0])
                else:
                    returnDict.append(np.array([0, 1]))
                    outcomes += np.array([0, 1])
                print("Game " + str(j) + " on Thread " + str(i) + " DONE")
                break

            _, move = moveSearchMax(board, depth, float("-inf"), float("inf"))

            # print("Move: ", move)

            board.push(move)
            #print_fen(board.fen().split(' ', 1)[0])
            #print("_________________")
            if board.is_game_over():
                print("IT'S ALL OVER")
                print(board.outcome().result())
                if board.outcome().winner is None:
                    returnDict.append(np.array([0.5, 0.5]))
                    outcomes += np.array([0.5, 0.5])
                elif board.outcome().winner:
                    returnDict.append(np.array([1, 0]))
                    outcomes += np.array([1, 0])
                else:
                    returnDict.append(np.array([0, 1]))
                    outcomes += np.array([0, 1])
                print("Game " + str(j) + " on Thread " + str(i) + " DONE")
                break
            #_ = input("press any key to continue")
        print(str(outcomes[0]) + "-" + str(outcomes[1]))
    print(str(i) + " done time: " + str(round(time.time() - t, 4)))


def main(to):
    board, board_fen = setup()

    depth = 4
    #print(depth, depth, depth)

    if to == "terminal":
        mainTerminal(board, board_fen, depth)
    elif to == "stocky":
        manager = Manager()
        return_dict = manager.list()
        jobs = []

        for i in range(10):
            p = Process(target=mainStocky, args=(i, return_dict, depth, time.time(),))
            jobs.append(p)
            p.start()

        for proc in jobs:
            proc.join()

        results = sum(return_dict)
        print(str(results[0]) + "-" + str(results[1]))
        #mainStocky(depth)
    elif to == "xboard":
        if input() == "xboard":
            sys.stdout.write("\n")
            sys.stdout.flush()
        else:
            raise Exception("not xboard")

        if input() == "protover 2":
            sys.stdout.write("\n")
            sys.stdout.flush()
        else:
            raise Exception("not protover 2")

        sys.stdout.write("feature done=0 reuse=0 time=0 sigint=0" + "\n")
        sys.stdout.flush()
        #sys.stdout.write("feature option=\"UCI_LimitStrength -check 1\"" + "\n")
        sys.stdout.write("feature done=1" + "\n")
        sys.stdout.flush()

        processInput(board, depth)

    return


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'terminal':
            main("terminal")
        elif sys.argv[1] == 'stocky':
            main("stocky")
        else:
            print("Usage: python engine.py terminal")
            raise Exception("Usage: python engine.py terminal")
    else:
        main("xboard")
