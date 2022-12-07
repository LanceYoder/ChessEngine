#!/usr/bin/env python

#-----------------------------------------------------------------------
# legalMoves.py
# Author: Lance Yoder
#-----------------------------------------------------------------------

import numpy as np

def legalMoves(FEN):
    moves = []
    boardArray, move, castle, enpassant, fifty, counter = FENtoBoardArray(FEN)

    for i in range(8):
        for j in range(8):
            moves.append()

#def legalMovesPiece(FEN, piece):
#    for

def FENtoBoardArray(FEN):
    boardArray = [["" for _ in range(8)] for _ in range(8)]
    fields = FEN.split(" ")

    i, j = 0, 0
    for c in fields[0]:
        if c == '/':
            i = 0
            j += 1
            continue
        if c.isdigit():
            i += int(c)
            print(i)
            continue
        boardArray[j][i] = c
        i += 1
    return boardArray, fields[1], fields[2], fields[3], int(fields[4]), int(fields[5])

def arrayPosToAN(x, y):
    return chr(x + 97) + chr(y + 49)


if __name__ == '__main__':
    print(FENtoBoardArray("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"))
    print(arrayPosToAN(0,0))
    print(arrayPosToAN(7, 7))
    print(arrayPosToAN(3, 4))
