#!/usr/bin/env python

#-----------------------------------------------------------------------
# engine.py
# Author: Lance Yoder
#-----------------------------------------------------------------------

import sys
import codecs
from utilities import *
from search import *

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

def main(to):
    board, board_fen = setup()

    depth = 4

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

    sys.stdout.write("feature done=0 reuse=0 time=0 sigint=0 done=1" + "\n")
    sys.stdout.flush()
    i = input()

    if i != "accepted done":
        raise Exception("not accepted done")
    if input() != "accepted reuse":
        raise Exception("not accepted reuse")
    if input() != "accepted time":
        raise Exception("not accepted time")
    if input() != "accepted sigint":
        raise Exception("not accepted sigint")
    if input() != "accepted done":
        raise Exception("not accepted done")
    if input() != "new":
        raise Exception("not new")
    if input() != "random":
        raise Exception("not random")
    if input().split(" ")[0] != "level":
        raise Exception("not level")
    if input() != "post":
        raise Exception("not post")
    if input() != "hard":
        raise Exception("not hard")


    if to == "terminal":
        mainTerminal(board, board_fen, depth)
    elif to == "xboard":
        processInput(board, depth)

    return


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'terminal':
            main("terminal")
        else:
            print("Usage: python engine.py terminal")
            raise Exception("Usage: python engine.py terminal")
    else:
        main("xboard")
