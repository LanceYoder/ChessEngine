import chess
import numpy as np
from globs import charToUni

def make_PV(length):
    PV = []
    neg = True
    for _ in range(length):
        if neg:
            PV.append((None, float("-inf")))
        else:
            PV.append((None, float("inf")))
        neg = not neg
    return PV

# return evaluation statistics. used for data fitting
def get_stats(board):
    # structure: queen#, rook#, bishop#, knight#, pawn#
    string = ""

    string += str(len(board.pieces(chess.QUEEN, chess.BLACK)) - len(board.pieces(chess.QUEEN, chess.WHITE)))
    string += ';'
    string += str(len(board.pieces(chess.ROOK, chess.BLACK)) - len(board.pieces(chess.ROOK, chess.WHITE)))
    string += ';'
    string += str(len(board.pieces(chess.BISHOP, chess.BLACK)) - len(board.pieces(chess.BISHOP, chess.WHITE)))
    string += ';'
    string += str(len(board.pieces(chess.KNIGHT, chess.BLACK)) - len(board.pieces(chess.KNIGHT, chess.WHITE)))
    string += ';'
    string += str(len(board.pieces(chess.PAWN, chess.BLACK)) - len(board.pieces(chess.PAWN, chess.WHITE)))
    string += ';'
    return string

# process input from xboard
def handle_input(board):

    INPUT = input()

    if INPUT == "white":
        print("Playing as white.")
        input()
        return "white"
    elif INPUT == "black":
        print("Playing as black.")
        return "black"

    try:
        move = chess.Move.from_uci(INPUT)
    except ValueError as ex:
        print(ex)
        return False

    board.push(move)
    return True

# print results of a game to terminal. records games for regressions
def handle_endgame(board, returnDict, outcomes, i):
    print("IT'S ALL OVER")
    out = board.outcome()
    winner = out.winner

    if winner is None:
        returnDict.append(np.array([0.5, 0.5]))
        outcomes += np.array([0.5, 0.5])
    elif winner ^ i % 2 != 0:
        returnDict.append(np.array([1, 0]))
        outcomes += np.array([1, 0])
    else:
        returnDict.append(np.array([0, 1]))
        outcomes += np.array([0, 1])
    print("Game 1 on Thread " + str(i) + " DONE")

# prints a fen as a textual board. used when playing
# in terminal
def print_fen(fen):
    rows = fen.split(' ')[0].split('/')
    print(rows)
    j = 0
    for row in rows:
        print(f'{8 - j} ', end='')
        j += 1
        for c in row:
            if c.isalpha():
                print(f'{charToUni[c]}', end=' ')
            else:
                for i in range(int(c)):
                    print('.', end=' ')
        print()
    print('  a b c d e f g h')

def setup():
    board = chess.Board()

    board_fen = board.fen().split(' ', 1)[0]

    return board, board_fen
