import chess
import chess.engine

DEPTH: int = 5

piece_values = {
    chess.PAWN: 100,
    chess.ROOK: 500,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.QUEEN: 900,
    chess.KING: 20000
}

piece_square_tables = {
    chess.PAWN: [0,   0,   0,   0,   0,   0,   0,   0,
                 78,  83,  86,  73, 102,  82,  85,  90,
                 7,  29,  21,  44,  40,  31,  44,   7,
                 -17,  16,  -2,  15,  14,   0,  15, -13,
                 -26,   3,  10,   9,   6,   1,   0, -23,
                 -22,   9,   5, -11, -10,  -2,   3, -19,
                 -31,   8,  -7, -37, -36, -14,   3, -31,
                 0,   0,   0,   0,   0,   0,   0,   0],
    chess.KNIGHT: [-66, -53, -75, -75, -10, -55, -58, -70,
                   -3,  -6, 100, -36,   4,  62,  -4, -14,
                   10,  67,   1,  74,  73,  27,  62,  -2,
                   24,  24,  45,  37,  33,  41,  25,  17,
                   -1,   5,  31,  21,  22,  35,   2,   0,
                   -18,  10,  13,  22,  18,  15,  11, -14,
                   -23, -15,   2,   0,   2,   0, -23, -20,
                   -74, -23, -26, -24, -19, -35, -22, -69],
    chess.BISHOP: [-59, -78, -82, -76, -23, -107, -37, -50,
                   -11,  20,  35, -42, -39,  31,   2, -22,
                   -9,  39, -32,  41,  52, -10,  28, -14,
                   25,  17,  20,  34,  26,  25,  15,  10,
                   13,  10,  17,  23,  17,  16,   0,   7,
                   14,  25,  24,  15,   8,  25,  20,  15,
                   19,  20,  11,   6,   7,   6,  20,  16,
                   -7,   2, -15, -12, -14, -15, -10, -10],
    chess.ROOK: [35,  29,  33,   4,  37,  33,  56,  50,
                 55,  29,  56,  67,  55,  62,  34,  60,
                 19,  35,  28,  33,  45,  27,  25,  15,
                 0,   5,  16,  13,  18,  -4,  -9,  -6,
                 -28, -35, -16, -21, -13, -29, -46, -30,
                 -42, -28, -42, -25, -25, -35, -26, -46,
                 -53, -38, -31, -26, -29, -43, -44, -53,
                 -30, -24, -18,   5,  -2, -18, -31, -32],
    chess.QUEEN: [6,   1,  -8, -104,  69,  24,  88,  26,
                  14,  32,  60, -10,  20,  76,  57,  24,
                  -2,  43,  32,  60,  72,  63,  43,   2,
                  1, -16,  22,  17,  25,  20, -13,  -6,
                  -14, -15,  -2,  -5,  -1, -10, -20, -22,
                  -30,  -6, -13, -11, -16, -11, -16, -27,
                  -36, -18,   0, -19, -15, -15, -21, -38,
                  -39, -30, -31, -13, -31, -36, -34, -42],
    chess.KING: [4,  54,  47, -99, -99,  60,  83, -62,
                 -32,  10,  55,  56,  56,  55,  10,   3,
                 -62,  12, -57,  44, -67,  28,  37, -31,
                 -55,  50,  11,  -4, -19,  13,   0, -49,
                 -55, -43, -52, -28, -51, -47,  -8, -50,
                 -47, -42, -43, -79, -64, -32, -29, -32,
                 -4,   3, -14, -50, -57, -18,  13,   4,
                 17,  30,  -3, -14,   6,  -1,  40,  18],
}

def evaluate_piece(piece, square):
    if piece.color == chess.WHITE:
        return piece_square_tables[piece.piece_type][square]
    else:
        return piece_square_tables[piece.piece_type][chess.square_mirror(square)]

def evaluate(board: chess.Board):
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -9999
        else:
            return 9999
        
    elif board.is_stalemate() or board.is_insufficient_material():
        return 0

    white_score = 0
    black_score = 0

    for square, piece in board.piece_map().items():
        piece_value = piece_values[piece.piece_type]
        square_eval = evaluate_piece(piece, square)
        if piece.color == chess.WHITE:
            white_score += piece_value + square_eval
        else:
            black_score += piece_value + square_eval

    return white_score - black_score


def minimax(board: chess.Board, depth, alpha, beta, maximizer):
    if depth == 0 or board.is_game_over():
        return evaluate(board)

    legal_moves = list(board.legal_moves)
    if maximizer:
        max_eval = -float('inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def find_best_move(board: chess.Board, depth):
    best_move = None
    best_value = -float('inf')
    alpha = -float('inf')
    beta = float('inf')

    for move in board.legal_moves:
        board.push(move)
        board_value = minimax(board, depth - 1, alpha, beta, False)
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
                moves = command.split("moves")[1].strip(
                ) if "moves" in command else ""
                for move in moves.split():
                    board.push_uci(move)

            elif "fen" in command:
                fen = command.split("position fen")[
                    1].strip().split(" moves")[0].strip()
                board.set_fen(fen)
                moves = command.split("moves")[1].strip(
                ) if "moves" in command else ""
                for move in moves.split():
                    board.push_uci(move)

        elif command.startswith("go"):
            move = find_best_move(board, DEPTH)
            print(f"bestmove {move.uci()}")

        elif command == "quit":
            break


if __name__ == "__main__":
    uci_loop()
