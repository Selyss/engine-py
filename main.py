import chess
import chess.engine

DEPTH: int = 5

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
        max_eval = -float('inf')
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


def find_best_move(board: chess.Board, depth):
    best_move = None
    best_value = -float('inf')
    for move in board.legal_moves:
        board.push(move)
        board_value = minimax(board, depth - 1, False)
        board.pop()
        if board_value > best_value:
            best_value = board_value
            best_move = move
    return best_move

# TODO: learn more about this uci wrapper
def uci_loop():
    board = chess.Board()
    while True:
        command = input()
        if command == "uci":
            print("id name engine-py")
            print("id author Selyss")
            print("uciok")

        elif command == "isready":
            print("readyok")

        elif command.startswith("position"):
            if "startpos" in command:
                board.set_fen(chess.STARTING_FEN)
                moves = command.split("moves")[1].strip() if "moves" in command else ""
                for move in moves.split():
                    board.push_uci(move)

            elif "fen" in command:
                fen = command.split("position fen")[1].strip().split(" moves")[0].strip()
                board.set_fen(fen)
                moves = command.split("moves")[1].strip() if "moves" in command else ""
                for move in moves.split():
                    board.push_uci(move)

        elif command.startswith("go"):
            move = find_best_move(board, DEPTH)
            print(f"bestmove {move.uci()}")

        elif command == "quit":
            break

if __name__ == "__main__":
    uci_loop()