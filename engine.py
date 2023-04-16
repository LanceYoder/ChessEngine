#!/usr/bin/env python

#-----------------------------------------------------------------------
# engine.py
# Author: Lance Yoder
#-----------------------------------------------------------------------

import sys
import codecs
#import time
from multiprocessing import Manager, Process

#from eval import game_phase
import time

import globs
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

def processInput(board, depth):
    gamephase = 0

    while True:
        if not handle_input(board):
            continue

        try:
            if board.is_game_over():
                continue


            mindepth = 1
            maxdepth = 5


            PV = make_PV(maxdepth)
            globs.pvLength = maxdepth

            for i in range(mindepth, maxdepth):
                print(i)
                _, PV = moveSearchMax(board, i, i, float("-inf"), float("inf"), globs.colorWhite, gamephase, PV, True)

            #_, move = moveSearchMax(board, 4, 4, float("-inf"), float("inf"), globs.colorWhite, gamephase)
            move = PV[0][0]
            board.push(move)
            gamephase = game_phase(board)

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
    gamephase = 0

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
            _, move = moveSearchMax(board, depth, depth, float("-inf"), float("inf"), globs.colorWhite, gamephase)
            #_, move = quiescence(board, depth, float("-inf"), float("inf"))

            print("Opponent's move: ", move)

            board.push(move)
            gamephase = game_phase(board)

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

    file = open('linreg.txt', 'a')



    for j in range(2):
        board, _ = setup()
        gamephase = 0
        print("Game " + str(j) + " on Thread " + str(i))
        k = 0
        while True:
            print(". Thread " + str(i) + " on Move " + str(k))
            k += 1
            move = takeStock(board.fen())

            move = chess.Move.from_uci(move)

            board.push(move)
            #print_fen(board.fen().split(' ', 1)[0])
            #print("_________________")

            if board.is_game_over():
                handle_endgame(board, returnDict, file, outcomes, i, j)
                break

            _, move = moveSearchMax(board, depth, depth, float("-inf"), float("inf"), False, gamephase)

            board.push(move)
            gamephase = game_phase(board)

            if board.is_game_over():
                handle_endgame(board, returnDict, file, outcomes, i, j)
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

        for i in range(4):
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
