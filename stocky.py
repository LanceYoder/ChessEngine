from stockfish import Stockfish
import os

def takeStock(fen, stockyElo=1500):

    path = os.environ.get('stockpath')
    stock = Stockfish(depth=10, parameters={"Debug Log File": path, "UCI_LimitStrength": "true", "UCI_Elo": stockyElo})
    stock.set_fen_position(fen)
    return stock.get_best_move()