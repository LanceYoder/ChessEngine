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

def pieceToScore(c):
    if c == 'P':  # caps are white
        return 1
    if c == 'R':
        return 5
    if c == 'N':
        return 3
    if c == 'B':
        return 3
    if c == 'Q':
        return 9
    if c == 'K':
        return 100
    if c == 'p':  # lowercase is black
        return -1
    if c == 'r':
        return -5
    if c == 'n':
        return -3
    if c == 'b':
        return -3
    if c == 'q':
        return -9
    if c == 'k':
        return -100
    print("c: ", c)
    return 1000
