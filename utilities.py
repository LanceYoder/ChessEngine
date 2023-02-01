import chess
from conversions import *

def print_fen(fen):
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

    board_fen = board.fen().split(' ', 1)[0]

    return board, board_fen
