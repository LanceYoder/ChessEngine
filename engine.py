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

    my_file = open("my_file.txt", "w")
    my_file.write(f'timeeex: {time.time()} \n')
    my_file.write("wrote input?")
    sys.stdout.write("in mainTerminal\n")
    sys.stdout.flush()

    board = chess.Board()

    boardfen = board.fen().split(' ', 1)[0]

    printfen(boardfen)
    print("------------------")

    while not board.is_game_over():
        try:
            INPUT = input("Move:\n")

            my_file.write("INput from xboard: ")
            my_file.write(INPUT)
            sys.stdout.write("input FFrom xboadD\n")
            sys.stdout.write(INPUT)
            sys.stdout.flush()
            print("Input from xboard: ", INPUT)

            move = chess.Move.from_uci(INPUT)
            while move not in board.legal_moves:
                INPUT = input("Not a legal move. Try again:\n")
                print("input: ", INPUT)
                move = chess.Move.from_uci(INPUT)

            board.push(move)

            if board.is_game_over():
                continue

            moves = board.generate_legal_moves()
            numlegal = board.legal_moves.count()
            num = np.random.randint(numlegal)
            i = 0
            for move in moves:
                if i == num:
                    damove = move
                    break
                i += 1
            board.push(damove)
            boardfen = board.fen().split(' ', 1)[0]

            printfen(boardfen)
            #print("------------------")
        except Exception as ex:
            print("oopss, ", ex)
            my_file.write("exception")

    boardfen = board.fen().split(' ', 1)[0]
    printfen(boardfen)
    if board.outcome().winner:
        print("White wins")
        my_file.write("White wins")
    else:
        print("Black wins")
        my_file.write("Black wins")

    my_file.close()

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
        inArray = INPUT.rsplit()
        try:
            move = chess.Move.from_uci(INPUT)
            board.push(move)

            moves = board.generate_legal_moves()
            numlegal = board.legal_moves.count()
            num = np.random.randint(numlegal)
            i = 0
            for move in moves:
                if i == num:
                    damove = move
                    break
                i += 1
            board.push(damove)
            #time.sleep(1)
            sys.stdout.write("move " + damove.uci() + "\n")
            sys.stdout.flush()
        except Exception as ex:
            sys.stdout.write(repr(ex) + "\n")
            sys.stdout.write(INPUT + "\n")
            sys.stdout.flush()
    return

def eval(board):




if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'terminal':
            mainTerminal()
        else:
            print("Usage: python engine.py terminal")
    else:
        main()
