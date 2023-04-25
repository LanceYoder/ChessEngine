#!/usr/bin/env python3

#-----------------------------------------------------------------------
# engine.py
# Author: Lance Yoder
#-----------------------------------------------------------------------

import sys
import codecs
#import time
from multiprocessing import Manager, Process
import multiprocessing as mp

import time

import globs
from globs import weight_sets
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

    colorWhite = False

    while True:
        success = handle_input(board)
        if success == "white":
            colorWhite = True
        elif not success:
            continue

        try:
            if board.is_game_over():
                continue

            PV = make_PV(depth)
            globs.pvLength = depth

            for i in range(1, depth):
                evaluation, PV = moveSearchMax(board, i, i, float("-inf"), float("inf"),
                                               colorWhite, gamephase, PV, True)

            move = PV[0][0]
            board.push(move)
            gamephase = game_phase(board)
            print("evaluation: ", evaluation)
            print("gamephase: ", gamephase)
            print_fen(board.fen())

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

        INPUT = input("Move:\n")

        colorWhite = False

        move = chess.Move.from_uci(INPUT)
        while move not in board.legal_moves:
            INPUT = input("Not a legal move. Try again:\n")
            print("input: ", INPUT)
            move = chess.Move.from_uci(INPUT)

        board.push(move)

        if board.is_game_over():
            continue

        PV = make_PV(depth)
        globs.pvLength = depth

        for i in range(1, depth):
            _, PV = moveSearchMax(board, i, i, float("-inf"), float("inf"),
                                  colorWhite, gamephase, PV, True)

        move = PV[0][0]
        board.push(move)
        gamephase = game_phase(board)

        print("Opponent's move: ", move)

        print_fen(board.fen().split(' ', 1)[0])


    board_fen = board.fen().split(' ', 1)[0]
    print_fen(board_fen)
    if board.outcome().winner:
        print("White wins")
    else:
        print("Black wins")

def mainStocky(i, returnDict, depth, t, stockyElo):
    outcomes = np.array([0.0, 0.0])
    globs.pvLength = depth

    try:
        board, _ = setup()
        gamephase = 0
        print("Game 1 on Thread " + str(i))

        if i % 2 == 0:
            move = takeStock(board.fen(), stockyElo=stockyElo)
            move = chess.Move.from_uci(move)
            board.push(move)

            colorWhite = False
            print("stockfish playing as white on Thread " + str(i))
        else:
            colorWhite = True
            print("stockfish playing as black on Thread " + str(i))

        k = 0
        while True:
            if k % 10 == 0:
                print(". Thread " + str(i) + " on Move " + str(k))
            k += 1

            PV = make_PV(depth)

            for dep in range(1, depth):
                _, PV = moveSearchMax(board, dep, dep, float("-inf"), float("inf"),
                                      colorWhite, gamephase, PV, True)

            move = PV#[0][0]
            board.push(move)
            gamephase = game_phase(board)

            if board.is_game_over():
                print("moves: ", k)
                handle_endgame(board, returnDict, outcomes, i)
                break

            move = takeStock(board.fen(), stockyElo=stockyElo)

            move = chess.Move.from_uci(move)

            board.push(move)

            if board.is_game_over():
                print("moves: ", k)
                handle_endgame(board, returnDict, outcomes, i)
                break

        print(str(outcomes[0]) + "-" + str(outcomes[1]))
    except Exception as ex:
        print(ex)
        raise ex

    print(str(i) + " done time: " + str(round(time.time() - t, 4)))

def mainSelf(i, returnDict, depth, t, set1, set2):
    outcomes = np.array([0.0, 0.0])

    try:
        board, _ = setup()
        gamephase = 0
        globs.pvLength = depth
        print("Game 1 on Thread " + str(i))

        if i % 2 == 0:

            PV = make_PV(depth)

            for dep in range(1, depth):
                _, PV = moveSearchMax(board, dep, dep, float("-inf"), float("inf"),
                                      True, gamephase, PV, True, set1=set2, set2=set1)

            move = PV[0][0]
            board.push(move)
            gamephase = game_phase(board)

            colorWhite = False
            firstSet = set2
            secondSet = set1
            print("set " + str(set2) + " playing as white, set " + str(set1) + " as black on Thread " + str(i))
        else:
            firstSet = set1
            secondSet = set2
            colorWhite = True
            print("set " + str(set1) + " playing as white, set " + str(set2) + " as black on Thread " + str(i))

        k = 0
        while True:
            if k % 10 == 0:
                print(". Thread " + str(i) + " on Move " + str(k))
            k += 1

            PV = make_PV(depth)

            for dep in range(1, depth):
                _, PV = moveSearchMax(board, dep, dep, float("-inf"), float("inf"), colorWhite,
                                      gamephase, PV, True, set1=firstSet, set2=secondSet)

            move = PV[0][0]
            board.push(move)
            gamephase = game_phase(board)

            #print_fen(board.fen().split(' ', 1)[0])

            if board.is_game_over():
                print("moves: ", k)
                handle_endgame(board, returnDict, outcomes, i)
                break

            PV = make_PV(depth)

            for dep in range(1, depth):
                _, PV = moveSearchMax(board, dep, dep, float("-inf"), float("inf"), not colorWhite,
                                      gamephase, PV, True, set1=firstSet, set2=secondSet)

            move = PV[0][0]
            board.push(move)
            gamephase = game_phase(board)

            if board.is_game_over():
                print("moves: ", k)
                handle_endgame(board, returnDict, outcomes, i)
                break

        print(str(outcomes[0]) + "-" + str(outcomes[1]))
    except Exception as ex:
        print(ex)
        raise ex

    print(str(i) + " done time: " + str(round(time.time() - t, 4)))

def main(to):
    board, board_fen = setup()

    depth = 5

    if to == "terminal":
        mainTerminal(board, board_fen, depth)

    elif to == "stocky":
        numGames = 2#int(sys.argv[2])
        stockyElo = 1500#int(sys.argv[3])

        #manager = Manager()
        #return_dict = manager.list()

        #num_workers = mp.cpu_count()

        #pool = mp.Pool(num_workers)

        errA = []


        #for i in range(numGames):
        #    errA.append(pool.apply_async(
        #        mainStocky, args=(i, return_dict, depth, time.time(), stockyElo,)))

        ret = []
        for _ in range(numGames):
            mainStocky(1, ret, depth, time.time(), stockyElo)

        for x in errA:
            x.get()

        #pool.close()
        #pool.join()

        results = sum(ret)
        print(str(results[0]) + "-" + str(results[1]))

    elif to == "self":
        numGames = int(sys.argv[2])
        set1 = sys.argv[3]
        set2 = sys.argv[4]

        manager = Manager()
        return_dict = manager.list()

        num_workers = mp.cpu_count()

        pool = mp.Pool(num_workers)

        errA = []

        for i in range(numGames):
            errA.append(pool.apply_async(
                mainSelf, args=(i, return_dict, depth, time.time(),
                                weight_sets[set1], weight_sets[set2],)))

        for x in errA:
            x.get()

        pool.close()
        pool.join()

        results = sum(return_dict)
        print(str(results[0]) + "-" + str(results[1]))

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
        elif sys.argv[1] == 'self':
            main("self")
        else:
            print("Usage: python engine.py ___")
            raise Exception("Usage: python engine.py ___")
    else:
        main("xboard")
