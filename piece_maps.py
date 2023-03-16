# all for white

def pms(piece_type, sqr):
    if piece_type == 'P':
        return pawn_pos(sqr)
    elif piece_type == 'p':
        return (-1) * pawn_pos(63 - sqr)
    elif piece_type == 'N':
        return knight_pos(sqr)
    elif piece_type == 'n':
        return (-1) * knight_pos(63 - sqr)
    elif piece_type == 'B':
        return bishop_pos(sqr)
    elif piece_type == 'b':
        return (-1) * bishop_pos(63 - sqr)
    elif piece_type == 'R':
        return rook_pos(sqr)
    elif piece_type == 'r':
        return (-1) * rook_pos(63 - sqr)
    elif piece_type == 'Q':
        return queen_pos(sqr)
    elif piece_type == 'q':
        return (-1) * queen_pos(63 - sqr)
    elif piece_type == 'K':
        return king_pos(sqr)
    elif piece_type == 'k':
        return (-1) * king_pos(63 - sqr)

# pawn
def pawn_pos(sqr):
              # a   b   c   d   e   f   g   h
    pawn_map = [0,  0,  0,  0,  0,  0,  0,  0, #1
                5, 10, 10,-20,-20, 10, 10,  5, #2
                5, -5,-10,  0,  0,-10, -5,  5, #3
                0,  0,  0, 20, 20,  0,  0,  0, #4
                5,  5, 10, 25, 25, 10,  5,  5, #5
               10, 10, 20, 30, 30, 20, 10, 10, #6
               50, 50, 50, 50, 50, 50, 50, 50, #7
                0,  0,  0,  0,  0,  0,  0,  0] #8
    return pawn_map[sqr]

# knight
def knight_pos(sqr):
    knight_map = [-50,-40,-30,-30,-30,-30,-40,-50,
                  -40,-20,  0,  5,  5,  0,-20,-40,
                  -30,  5, 10, 15, 15, 10,  5,-30,
                  -30,  0, 15, 20, 20, 15,  0,-30,
                  -30,  5, 15, 20, 20, 15,  5,-30,
                  -30,  0, 10, 15, 15, 10,  0,-30,
                  -40,-20,  0,  0,  0,  0,-20,-40,
                  -50,-40,-30,-30,-30,-30,-40,-50]

    return knight_map[sqr]

# bishop
def bishop_pos(sqr):
    bishop_map = [-20,-10,-10,-10,-10,-10,-10,-20,
                  -10,  5,  0,  0,  0,  0,  5,-10,
                  -10, 10, 10, 10, 10, 10, 10,-10,
                  -10,  0, 10, 10, 10, 10,  0,-10,
                  -10,  5,  5, 10, 10,  5,  5,-10,
                  -10,  0,  5, 10, 10,  5,  0,-10,
                  -10,  0,  0,  0,  0,  0,  0,-10,
                  -20,-10,-10,-10,-10,-10,-10,-20]

    return bishop_map[sqr]

# rook
def rook_pos(sqr):
    rook_map = [0,  0,  0,  5,  5,  0,  0,  0,
               -5,  0,  0,  0,  0,  0,  0, -5,
               -5,  0,  0,  0,  0,  0,  0, -5,
               -5,  0,  0,  0,  0,  0,  0, -5,
               -5,  0,  0,  0,  0,  0,  0, -5,
               -5,  0,  0,  0,  0,  0,  0, -5,
                5, 10, 10, 10, 10, 10, 10,  5,
                0,  0,  0,  0,  0,  0,  0,  0]

    return rook_map[sqr]

# queen
def queen_pos(sqr):
    queen_map = [-20,-10,-10, -5, -5,-10,-10,-20,
                 -10,  0,  5,  0,  0,  0,  0,-10,
                 -10,  5,  5,  5,  5,  5,  0,-10,
                   0,  0,  5,  5,  5,  5,  0, -5,
                  -5,  0,  5,  5,  5,  5,  0, -5,
                 -10,  0,  5,  5,  5,  5,  0,-10,
                 -10,  0,  0,  0,  0,  0,  0,-10,
                 -20,-10,-10, -5, -5,-10,-10,-20]

    return queen_map[sqr]

# king
def king_pos(sqr):
    king_map = [20, 30, 10,  0,  0, 10, 30, 20,
                20, 20,  0,  0,  0,  0, 20, 20,
               -10,-20,-20,-20,-20,-20,-20,-10,
               -20,-30,-30,-40,-40,-30,-30,-20,
               -30,-40,-40,-50,-50,-40,-40,-30,
               -30,-40,-40,-50,-50,-40,-40,-30,
               -30,-40,-40,-50,-50,-40,-40,-30,
               -30,-40,-40,-50,-50,-40,-40,-30]

    return king_map[sqr]

