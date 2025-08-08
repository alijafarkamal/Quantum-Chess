import chess

PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}

def evaluate_move(board, move):
    board_copy = board.copy()
    board_copy.push(move)
    
    material_score = 0
    
    for square in chess.SQUARES:
        piece = board_copy.piece_at(square)
        if piece:
            value = PIECE_VALUES[piece.piece_type]
            if piece.color == chess.WHITE:
                material_score += value
            else:
                material_score -= value
    
    if board.turn == chess.BLACK:
        material_score = -material_score
    
    return material_score

def get_move_quality_score(board, move):
    board_copy = board.copy()
    board_copy.push(move)
    
    base_score = evaluate_move(board, move)
    
    bonus = 0
    
    if board_copy.is_checkmate():
        bonus += 1000
    elif board_copy.is_check():
        bonus += 50
    
    if board_copy.is_capture(board_copy.peek()):
        bonus += 10
    
    return base_score + bonus 