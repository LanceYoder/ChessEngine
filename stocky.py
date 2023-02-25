from stockfish import Stockfish
import chess

#stockfi = Stockfish(depth=10, parameters={"Debug Log File": "/Users/lanceyoder/ChessEngine/destock.txt",  "Skill Level": 20})

#stockfi.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

#print(stockfi.get_best_move())

def takeStock(board, fen):
    stock = Stockfish(depth=10, parameters={"Debug Log File": "/Users/lanceyoder/ChessEngine/destock.txt", "UCI_LimitStrength": "true", "UCI_Elo": 1700})
    stock.set_fen_position(fen)
    #print(stock.get_best_move())
    return stock.get_best_move()