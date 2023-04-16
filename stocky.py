from stockfish import Stockfish
import chess

def takeStock(fen):
    stock = Stockfish(depth=10, parameters={"Debug Log File": "/Users/lanceyoder/ChessEngine/destock.txt", "UCI_LimitStrength": "true", "UCI_Elo": 1560})
    stock.set_fen_position(fen)
    return stock.get_best_move()