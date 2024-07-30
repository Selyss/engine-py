import chess
import chess.engine

DEPTH: int = 4

piece_values = {
    chess.PAWN: 100,
    chess.ROOK: 500,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.QUEEN: 900,
    chess.KING: 20000
}


def evaluate(board: chess.Board):
    white_material = sum([piece_values[piece.piece_type] for piece in board.piece_map().values() if piece.color == chess.WHITE])
    black_material = sum([piece_values[piece.piece_type] for piece in board.piece_map().values() if piece.color == chess.BLACK])

    return float(white_material - black_material)

    
def minimax(board: chess.Board, depth, maximizer):
    if depth == 0 or board.is_game_over():
        return evaluate(board)
    
    if maximizer:
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, False)
            max_eval = max(max_eval, eval)
            board.pop()
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, True)
            min_eval = min(min_eval, eval)
            board.pop()
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