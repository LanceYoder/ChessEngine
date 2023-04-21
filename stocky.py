from stockfish import Stockfish

def takeStock(fen, stockyElo=1500):
    stock = Stockfish(depth=10, parameters={"Debug Log File": "/home/lanceyoder/ChessEngine/destock.txt", "UCI_LimitStrength": "true", "UCI_Elo": stockyElo})
    stock.set_fen_position(fen)
    return stock.get_best_move()