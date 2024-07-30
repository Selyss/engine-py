import chess
import chess.engine

board = chess.Board(chess.STARTING_FEN)

def evaluate(board: chess.Board):
    white_material = sum([piece_value(piece) for piece in board.piece_map().values() if piece.color == chess.WHITE])
    black_material = sum([piece_value(piece) for piece in board.piece_map().values() if piece.color == chess.BLACK])

    return float(white_material - black_material)


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
    
def minimax(board: chess.Board, depth, maximizer):
    if depth == 0 or board.is_game_over():
        return evaluate(board)
    
    legal_moves = list(board.legal_moves)

    if maximizer:
        value = -float('inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, False)
            board.pop()
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, True)
            board.pop()
            min_eval = min(min_eval, eval)
        return min_eval

print(evaluate(board))