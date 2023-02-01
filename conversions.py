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

def pieceToScore(c):
    if c == 'P':  # caps are white
        return 10
    elif c == 'R':
        return 50
    elif c == 'N':
        return 30
    elif c == 'B':
        return 30
    elif c == 'Q':
        return 90
    elif c == 'K':
        return 1000
    elif c == 'p':  # lowercase is black
        return -10
    elif c == 'r':
        return -50
    elif c == 'n':
        return -30
    elif c == 'b':
        return -30
    elif c == 'q':
        return -90
    elif c == 'k':
        return -1000
    print("c: ", c)
    return 10000
