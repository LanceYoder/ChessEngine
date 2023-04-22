import chess
import numpy as np
import globs

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
def handle_endgame(board, returnDict, outcomes, i, j):
    print("IT'S ALL OVER")
    out = board.outcome()
    winner = out.winner

    if winner is None:
        returnDict.append(np.array([0.5, 0.5]))
        outcomes += np.array([0.5, 0.5])
    elif winner ^ (i+j) % 2 != 0:
        returnDict.append(np.array([1, 0]))
        outcomes += np.array([1, 0])
    else:
        returnDict.append(np.array([0, 1]))
        outcomes += np.array([0, 1])
    print("Game " + str(j) + " on Thread " + str(i) + " DONE")

# convert characters to unicode. used for printing to termianl
def charToUni(c):
    if c == 'P':
        return u'\N{WHITE CHESS PAWN}'
    elif c == 'R':
        return u'\N{WHITE CHESS ROOK}'
    elif c == 'N':
        return u'\N{WHITE CHESS KNIGHT}'
    elif c == 'B':
        return u'\N{WHITE CHESS BISHOP}'
    elif c == 'Q':
        return u'\N{WHITE CHESS QUEEN}'
    elif c == 'K':
        return u'\N{WHITE CHESS KING}'
    elif c == 'p':
        return u'\N{BLACK CHESS PAWN}'
    elif c == 'r':
        return u'\N{BLACK CHESS ROOK}'
    elif c == 'n':
        return u'\N{BLACK CHESS KNIGHT}'
    elif c == 'b':
        return u'\N{BLACK CHESS BISHOP}'
    elif c == 'q':
        return u'\N{BLACK CHESS QUEEN}'
    elif c == 'k':
        return u'\N{BLACK CHESS KING}'

# return piece weights based on chars
def pieceToScore(c):
    if c == 'P':  # caps are white
        return 100
    elif c == 'R':
        return 500
    elif c == 'N':
        return 300
    elif c == 'B':
        return 300
    elif c == 'Q':
        return 900
    elif c == 'K':
        return 10000
    elif c == 'p':  # lowercase is black
        return -100
    elif c == 'r':
        return -500
    elif c == 'n':
        return -300
    elif c == 'b':
        return -300
    elif c == 'q':
        return -900
    elif c == 'k':
        return -10000
    print("c: ", c)
    return 10000

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
