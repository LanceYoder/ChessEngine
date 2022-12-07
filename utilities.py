import chess
from conversions import *

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


def setup():
    board = chess.Board()

    boardfen = board.fen().split(' ', 1)[0]

    return board, boardfen