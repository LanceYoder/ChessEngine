#!/usr/bin/env python

#-----------------------------------------------------------------------
# chessboard.py
# Author: Lance Yoder
#-----------------------------------------------------------------------

class piece:
    def __init__(self, type, color, pos):
        self.type = type.lower()
        self.color = color
        self.pos = pos
        if color == "black":
            self.repr = type.upper()
        else:
            self.repr = type.lower()

class chessboard:
    def __init__(self, FEN):
        self.FEN = FEN

    def toFen():

        return FEN