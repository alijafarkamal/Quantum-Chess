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

def evaluate_board_state(board, player_color):
    """
    Calculates a comprehensive static score for a board position.
    A positive score favors the player whose turn it is.
    """
    if board.is_checkmate():
        return -10000 if board.turn == player_color else 10000
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    # 1. Material Advantage
    piece_values = {chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330, chess.ROOK: 500, chess.QUEEN: 900}
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = piece_values.get(piece.piece_type, 0)
            if piece.color == player_color:
                score += value
            else:
                score -= value
    
    # 2. Mobility: Number of legal moves
    mobility = len(list(board.legal_moves))
    score += 10 * mobility

    # 3. King safety
    if board.is_check():
        score -= 50
    
    # 4. Center control (simplified)
    center_squares = [chess.E4, chess.E5, chess.D4, chess.D5]
    center_control = 0
    for square in center_squares:
        if board.piece_at(square):
            piece = board.piece_at(square)
            if piece.color == player_color:
                center_control += 5
            else:
                center_control -= 5
    score += center_control

    # 5. Pawn structure (simplified)
    pawn_structure = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece and piece.piece_type == chess.PAWN:
            if piece.color == player_color:
                # Bonus for advanced pawns
                rank = chess.square_rank(square)
                if player_color == chess.WHITE:
                    pawn_structure += rank * 10
                else:
                    pawn_structure += (7 - rank) * 10
    score += pawn_structure

    # 6. Piece activity
    piece_activity = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece and piece.color == player_color:
            # Bonus for pieces in the center
            file = chess.square_file(square)
            rank = chess.square_rank(square)
            if 2 <= file <= 5 and 2 <= rank <= 5:
                piece_activity += 5
    score += piece_activity

    # 7. Development (for early game)
    development = 0
    if board.fullmove_number <= 10:
        # Bonus for developed pieces
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.color == player_color:
                if piece.piece_type in [chess.KNIGHT, chess.BISHOP]:
                    rank = chess.square_rank(square)
                    if piece.color == chess.WHITE and rank > 1:
                        development += 10
                    elif piece.color == chess.BLACK and rank < 6:
                        development += 10
    score += development

    return score 