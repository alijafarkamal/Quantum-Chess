import networkx as nx
import chess
import numpy as np
from chess_logic.move_eval import get_move_quality_score
from quantum.quantum_walk import evaluate_position_with_true_qwalk, generate_move_graph

class QuantumWalkEvaluator:
    def __init__(self, max_depth=3, max_breadth=10):
        self.max_depth = max_depth
        self.max_breadth = max_breadth
    
    def quantum_walk_score(self, board, depth=None):
        """
        Use the new true quantum walk implementation.
        """
        if depth is None:
            depth = self.max_depth
        
        # Use the new true quantum walk evaluation
        move_scores = evaluate_position_with_true_qwalk(board, depth)
        
        if not move_scores:
            return None
        
        # Find the best move based on scores
        best_move_uci = max(move_scores, key=move_scores.get)
        
        # Convert UCI string back to move object
        for move in board.legal_moves:
            if move.uci() == best_move_uci:
                return move
        
        return None
    
    def evaluate_position_quality(self, board):
        material_score = 0
        mobility_score = 0
        safety_score = 0
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                value = self.get_piece_value(piece.piece_type)
                if piece.color == chess.WHITE:
                    material_score += value
                else:
                    material_score -= value
        
        mobility_score = len(list(board.legal_moves))
        if board.turn == chess.BLACK:
            mobility_score = -mobility_score
        
        safety_score = 0
        if board.is_check():
            safety_score = -50
        elif board.is_checkmate():
            safety_score = -1000
        
        return material_score + mobility_score * 0.1 + safety_score
    
    def get_piece_value(self, piece_type):
        values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }
        return values.get(piece_type, 0)
    
    def quantum_amplitude_score(self, board, move, depth=2):
        """
        Enhanced quantum amplitude scoring using true quantum walk.
        """
        board_copy = board.copy()
        board_copy.push(move)
        
        # Use the new quantum walk evaluation for the resulting position
        move_scores = evaluate_position_with_true_qwalk(board_copy, depth)
        
        if move_scores:
            # Return the average score of all possible responses
            return np.mean(list(move_scores.values()))
        else:
            # Fallback to heuristic evaluation
            return self.evaluate_position_quality(board_copy)
    
    def select_best_move_quantum_walk(self, board, legal_moves):
        """
        Select best move using the new true quantum walk.
        """
        if not legal_moves:
            return None
        
        if len(legal_moves) == 1:
            return legal_moves[0]
        
        # Use the new quantum walk evaluation
        move_scores = evaluate_position_with_true_qwalk(board, self.max_depth)
        
        if not move_scores:
            # Fallback to classical evaluation
            best_move = None
            best_score = float('-inf')
            
            for move in legal_moves:
                score = self.quantum_amplitude_score(board, move, self.max_depth)
                if score > best_score:
                    best_score = score
                    best_move = move
            
            return best_move
        
        # Find the best move from quantum walk results
        best_move_uci = max(move_scores, key=move_scores.get)
        
        for move in legal_moves:
            if move.uci() == best_move_uci:
                return move
        
        # Fallback if move not found
        return legal_moves[0]
    
    def get_quantum_walk_probabilities(self, board, depth=2):
        """
        Get probability distribution from quantum walk.
        """
        # Generate graph and run quantum walk
        adj_list, fen_to_idx, idx_to_fen, move_tree = generate_move_graph(board, depth)
        
        if not adj_list:
            return {}
        
        start_fen = board.fen()
        start_idx = fen_to_idx.get(start_fen, 0)
        
        # Run quantum walk
        from quantum.quantum_walk import run_true_quantum_walk
        final_counts = run_true_quantum_walk(adj_list, start_idx, steps=depth)
        
        # Convert to probabilities
        total_counts = sum(final_counts.values())
        if total_counts == 0:
            return {}
        
        probabilities = {}
        for node_idx, count in final_counts.items():
            if node_idx in idx_to_fen:
                fen = idx_to_fen[node_idx]
                probabilities[fen] = count / total_counts
        
        return probabilities 