
# piece type to ASCII for printing to terminal
charToUni = {'P': u'\N{WHITE CHESS PAWN}', 'N': u'\N{WHITE CHESS KNIGHT}', 'B': u'\N{WHITE CHESS BISHOP}',
     'R': u'\N{WHITE CHESS ROOK}', 'Q': u'\N{WHITE CHESS QUEEN}', 'K': u'\N{WHITE CHESS KING}',
     'p': u'\N{BLACK CHESS PAWN}', 'n': u'\N{BLACK CHESS KNIGHT}', 'b': u'\N{BLACK CHESS BISHOP}',
     'r': u'\N{BLACK CHESS ROOK}', 'q': u'\N{BLACK CHESS QUEEN}', 'k': u'\N{BLACK CHESS KING}'}

# record depth of PV tables
pvLength = 0

# piece weighting sets
bado = {'P':-100, 'N':-100, 'B':-100, 'R':-100, 'Q':-1000, 'K':100000, 'p':100, 'n':100, 'b':100, 'r':100, 'q':1000, 'k':-100000}
traditional = {'P':100, 'N':300, 'B':300, 'R':500, 'Q':900, 'K':100000, 'p':-100, 'n':-300, 'b':-300, 'r':-500, 'q':-900, 'k':-100000}
michniewski = {'P':100, 'N':320, 'B':330, 'R':500, 'Q':900, 'K':100000, 'p':-100, 'n':-320, 'b':-330, 'r':-500, 'q':-900, 'k':-100000}
kaufman = {'P':100, 'N':350, 'B':350, 'R':525, 'Q':1000, 'K':100000, 'p':-100, 'n':-350, 'b':-350, 'r':-525, 'q':-1000, 'k':-100000}
fruit = {'P':100, 'N':400, 'B':400, 'R':600, 'Q':1200, 'K':100000, 'p':-100, 'n':-400, 'b':-400, 'r':-600, 'q':-1200, 'k':-100000}
alphazero = {'P':100, 'N':305, 'B':333, 'R':563, 'Q':950, 'K':100000, 'p':-100, 'n':-303, 'b':-333, 'r':-563, 'q':-950, 'k':-100000}

weight_sets = {"bado": bado, "traditional": traditional, "michniewski": michniewski, "kaufman": kaufman,
               "fruit": fruit, "alphazero": alphazero}