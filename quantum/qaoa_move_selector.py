import numpy as np
import chess
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from chess_logic.move_eval import get_move_quality_score

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

    return score

def create_simple_qaoa_circuit(move_scores, gamma=1.0, beta=1.0):
    """
    Creates a simple QAOA circuit for move selection.
    """
    num_moves = len(move_scores)
    if num_moves == 0:
        return None
    
    # Create quantum circuit
    qc = QuantumCircuit(num_moves, num_moves)
    
    # Initialize in equal superposition
    for i in range(num_moves):
        qc.h(i)
    
    # Apply cost Hamiltonian (phase separator)
    for i in range(num_moves):
        qc.rz(gamma * move_scores[i], i)
    
    # Apply mixing Hamiltonian
    for i in range(num_moves):
        qc.rx(beta, i)
    
    # Measure
    qc.measure_all()
    
    return qc

def select_move_with_qaoa(board, shots=1024):
    """
    Selects the best move using a simplified QAOA approach.
    """
    legal_moves = list(board.legal_moves)
    if not legal_moves:
        return None, {}

    if len(legal_moves) == 1:
        return legal_moves[0], {legal_moves[0].uci(): 1.0}

    # 1. Evaluate the outcome of each legal move
    move_scores = []
    for move in legal_moves:
        temp_board = board.copy()
        temp_board.push(move)
        score = evaluate_board_state(temp_board, board.turn)
        move_scores.append(score)

    # Normalize scores to be positive
    min_score = min(move_scores)
    if min_score < 0:
        move_scores = [s - min_score + 1 for s in move_scores]

    # 2. Create and run QAOA circuit
    try:
        # Try different parameter combinations
        best_result = None
        best_prob = 0
        
        for gamma in [0.5, 1.0, 1.5]:
            for beta in [0.5, 1.0, 1.5]:
                qc = create_simple_qaoa_circuit(move_scores, gamma, beta)
                if qc is None:
                    continue
                
                # Execute circuit
                backend = Aer.get_backend('qasm_simulator')
                job = backend.run(qc, shots=shots)
                counts = job.result().get_counts()
                
                # Find the bitstring with highest probability
                for bitstring, count in counts.items():
                    prob = count / shots
                    if prob > best_prob:
                        best_prob = prob
                        best_result = bitstring
        
        if best_result:
            # Find the move corresponding to the best bitstring
            best_move_index = best_result.rfind('1')
            if best_move_index != -1 and best_move_index < len(legal_moves):
                best_move = legal_moves[best_move_index]
                
                # Create probability map
                prob_map = {}
                for bitstring, count in counts.items():
                    move_index = bitstring.rfind('1')
                    if move_index != -1 and move_index < len(legal_moves):
                        move_uci = legal_moves[move_index].uci()
                        prob_map[move_uci] = count / shots
                
                return best_move, prob_map
        
        # Fallback: return move with highest score
        best_index = np.argmax(move_scores)
        best_move = legal_moves[best_index]
        prob_map = {best_move.uci(): 1.0}
        return best_move, prob_map
        
    except Exception as e:
        print(f"QAOA failed, falling back to classical: {e}")
        # Fallback to classical selection
        best_index = np.argmax(move_scores)
        best_move = legal_moves[best_index]
        prob_map = {best_move.uci(): 1.0}
        return best_move, prob_map

def qaoa_move_selector(board, legal_moves):
    """
    Wrapper function for QAOA move selection.
    """
    try:
        return select_move_with_qaoa(board)
    except Exception as e:
        print(f"QAOA move selector failed, falling back to classical: {e}")
        # Fallback to simple evaluation
        best_move = None
        best_score = float('-inf')
        
        for move in legal_moves:
            score = get_move_quality_score(board, move)
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move, {best_move.uci(): 1.0} if best_move else (None, {}) 