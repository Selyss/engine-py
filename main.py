import chess
import chess.engine

DEPTH: int = 4

### Tables, piece values, and piece eval from https://github.com/healeycodes/andoma/blob/main/evaluate.py

piece_values = {
    chess.PAWN: 100,
    chess.ROOK: 500,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.QUEEN: 900,
    chess.KING: 20000
}

pawnEvalWhite = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, -20, -20, 10, 10,  5,
    5, -5, -10,  0,  0, -10, -5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5,  5, 10, 25, 25, 10,  5,  5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0
]
pawnEvalBlack = list(reversed(pawnEvalWhite))

knightEval = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]

bishopEvalWhite = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]
bishopEvalBlack = list(reversed(bishopEvalWhite))

rookEvalWhite = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0
]
rookEvalBlack = list(reversed(rookEvalWhite))

queenEval = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -5, 0, 5, 5, 5, 5, 0, -5,
    0, 0, 5, 5, 5, 5, 0, -5,
    -10, 5, 5, 5, 5, 5, 0, -10,
    -10, 0, 5, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20
]

kingEvalWhite = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30
]

kingEvalBlack = list(reversed(kingEvalWhite))


def evaluate_piece(piece: chess.Piece, square: chess.Square):
    mapping = []
    if piece.piece_type == chess.PAWN:
        mapping = pawnEvalWhite if piece.color == chess.WHITE else pawnEvalBlack
    if piece.piece_type == chess.KNIGHT:
        mapping = knightEval
    if piece.piece_type == chess.BISHOP:
        mapping = bishopEvalWhite if piece.color == chess.WHITE else bishopEvalBlack
    if piece.piece_type == chess.ROOK:
        mapping = rookEvalWhite if piece.color == chess.WHITE else rookEvalBlack
    if piece.piece_type == chess.QUEEN:
        mapping = queenEval
    if piece.piece_type == chess.KING:
        # TODO: add endgame eval
        mapping = kingEvalWhite if piece.color == chess.WHITE else kingEvalBlack
    
    return mapping[square]
    

def evaluate(board: chess.Board):
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -9999
        else:
            return 9999
        
    elif board.is_stalemate() or board.is_insufficient_material():
        return 0

    overall_eval = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if not piece:
            continue

        piece_eval = piece_values[piece.piece_type] 
        square_eval = evaluate_piece(piece, square)

        eval = piece_eval + square_eval
        overall_eval += eval if piece.color == chess.WHITE else -eval

    return overall_eval


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


def find_best_move_and_evaluation(board: chess.Board, depth):
    best_move = None
    best_value = -float('inf')
    alpha = -float('inf')
    beta = float('inf')

    for move in board.legal_moves:
        board.push(move)
        board_value = minimax(board, depth - 1, alpha, beta, board.turn == chess.BLACK)
        board.pop()
        if board_value > best_value:
            best_value = board_value
            best_move = move
    return best_move, best_value

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
            best_move, evaluation = find_best_move_and_evaluation(board, DEPTH)
            print(f"bestmove {best_move.uci()}")
            print(f"info score cp {evaluation}")

        elif command == "quit":
            break


if __name__ == "__main__":
    uci_loop()
