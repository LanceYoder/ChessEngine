#!/usr/bin/env python

#-----------------------------------------------------------------------
# engine.py
# Author: Lance Yoder
#-----------------------------------------------------------------------

import sys
import codecs
from multiprocessing import Manager, Process

from utilities import *
from search import *
from stocky import *

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

gamePhase = 0

def handle_input():

    while True:

        try:
            INPUT = input()
        except KeyboardInterrupt as ex:
            sys.stdout.write(str(ex))
            sys.stdout.flush()
            continue

        if INPUT.split(" ")[0] == "time" or INPUT.split(" ")[0] == "otim":
            continue

        return INPUT

def processInput(board, depth):
    while True:

        INPUT = handle_input()

        try:
            move = chess.Move.from_uci(INPUT)

            board.push(move)

            if board.is_game_over():
                continue

            # black should want a very negative score, white a very positive score
            #sys.stdout.write("len")
            #sys.stdout.write(str(len(board.piece_map())))
            #sys.stdout.flush()
            if len(board.piece_map()) < 10:
                depth = 6

            _, move = moveSearchMax(board, depth, float("-inf"), float("inf"))

            #print("Move: ", move)

            board.push(move)

            sys.stdout.write("move " + move.uci() + "\n")
            sys.stdout.flush()
        except Exception as ex:
            sys.stdout.write(repr(ex) + "\n")
            sys.stdout.write(INPUT + "\n")
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

def mainStocky(i, returnDict, depth):
    outcomes = np.array([0.0, 0.0])

    for j in range(4):
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


def main(to):
    board, board_fen = setup()

    depth = 4

    if to == "terminal":
        mainTerminal(board, board_fen, depth)
    elif to == "stocky":
        manager = Manager()
        return_dict = manager.list()
        jobs = []

        for i in range(10):
            p = Process(target=mainStocky, args=(i, return_dict, depth,))
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
        sys.stdout.write("feature option=\"UCI_LimitStrength -check 1\"" + "\n")
        sys.stdout.write("feature done=1" + "\n")
        sys.stdout.flush()

        i = input()
        if i != "accepted done":
            raise Exception("not accepted done", i)
        i = input()
        if i != "accepted reuse":
            raise Exception("not accepted reuse", i)
        i = input()
        if i != "accepted time":
            raise Exception("not accepted time", i)
        i = input()
        if i != "accepted sigint":
            raise Exception("not accepted sigint", i)
        i = input()
        if i != "accepted option":
            raise Exception("not accepted option", i)
        i = input()
        if i != "accepted done":
            raise Exception("not accepted done", i)
        i = input()
        if i != "new":
            raise Exception("not new", i)
        i = input()
        if i != "random":
            raise Exception("not random", i)
        i = input()
        if i.split(" ")[0] != "level":
            raise Exception("not level", i)
        i = input()
        if i != "post":
            raise Exception("not post", i)
        i = input()
        if i != "hard":
            raise Exception("not hard", i)


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
