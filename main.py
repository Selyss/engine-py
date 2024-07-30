import chess
import chess.engine

board = chess.Board(chess.STARTING_FEN)

def evaluate(board: chess.Board):
    white_material = sum([piece_value(piece) for piece in board.piece_map().values() if piece.color == chess.WHITE])
    black_material = sum([piece_value(piece) for piece in board.piece_map().values() if piece.color == chess.BLACK])

    return white_material - black_material


def piece_value(piece):
    if piece.piece_type == chess.PAWN:
        return 1
    elif piece.piece_type == chess.KNIGHT:
        return 3
    elif piece.piece_type == chess.BISHOP:
        return 3
    elif piece.piece_type == chess.ROOK:
        return 5
    elif piece.piece_type == chess.QUEEN:
        return 9
    else:
        return 0

print(evaluate(board))