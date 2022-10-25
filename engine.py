#!/usr/bin/env python

#-----------------------------------------------------------------------
# engine.py
# Author: Lance Yoder
#-----------------------------------------------------------------------

import chess
import numpy as np

import sys, codecs

if sys.stdout.encoding is None or sys.stdout.encoding == 'ANSI_X3.4-1968':
    utf8_writer = codecs.getwriter('UTF-8')
    if sys.version_info.major < 3:
        sys.stdout = utf8_writer(sys.stdout, errors='replace')
    else:
        sys.stdout = utf8_writer(sys.stdout.buffer, errors='replace')

def charToUni(c):
    match c:
        case 'P':
            return u'\N{WHITE CHESS PAWN}'
        case 'R':
            return u'\N{WHITE CHESS ROOK}'
        case 'N':
            return u'\N{WHITE CHESS KNIGHT}'
        case 'B':
            return u'\N{WHITE CHESS BISHOP}'
        case 'Q':
            return u'\N{WHITE CHESS QUEEN}'
        case 'K':
            return u'\N{WHITE CHESS KING}'
        case 'p':
            return u'\N{BLACK CHESS PAWN}'
        case 'r':
            return u'\N{BLACK CHESS ROOK}'
        case 'n':
            return u'\N{BLACK CHESS KNIGHT}'
        case 'b':
            return u'\N{BLACK CHESS BISHOP}'
        case 'q':
            return u'\N{BLACK CHESS QUEEN}'
        case 'k':
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
        print("------------------")
    except Exception as ex:
        print("Oops: ", ex)

boardfen = board.fen().split(' ', 1)[0]
printfen(boardfen)
if board.outcome().winner:
    print("White wins")
else:
    print("Black wins")










