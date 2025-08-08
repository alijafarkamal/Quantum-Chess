import chess

def get_board_from_fen(fen_string):
    try:
        board = chess.Board(fen_string)
        return board
    except ValueError as e:
        raise ValueError(f"Invalid FEN string: {e}")

def apply_move_to_board(board, move):
    new_board = board.copy()
    new_board.push(move)
    return new_board

def get_fen_from_board(board):
    return board.fen()

def is_valid_fen(fen_string):
    try:
        chess.Board(fen_string)
        return True
    except ValueError:
        return False

def get_board_info(board):
    info = {
        'turn': 'White' if board.turn else 'Black',
        'castling_rights': str(board.castling_rights),
        'en_passant': str(board.ep_square) if board.ep_square else 'None',
        'halfmove_clock': board.halfmove_clock,
        'fullmove_number': board.fullmove_number,
        'legal_moves_count': len(list(board.legal_moves)),
        'is_check': board.is_check(),
        'is_checkmate': board.is_checkmate(),
        'is_stalemate': board.is_stalemate(),
        'is_insufficient_material': board.is_insufficient_material()
    }
    return info 