import networkx as nx
import chess
import numpy as np
from chess_logic.move_eval import get_move_quality_score

class QuantumWalkEvaluator:
    def __init__(self, max_depth=3, max_breadth=10):
        self.max_depth = max_depth
        self.max_breadth = max_breadth
    
    def quantum_walk_score(self, board, depth=None):
        if depth is None:
            depth = self.max_depth
        
        G = nx.DiGraph()
        position_scores = {}
        
        def build_graph(node, current_board, current_depth, path_score=0):
            if current_depth == 0:
                position_scores[node] = path_score
                return
            
            legal_moves = list(current_board.legal_moves)
            if not legal_moves:
                position_scores[node] = path_score
                return
            
            for move in legal_moves[:self.max_breadth]:
                current_board.push(move)
                next_fen = current_board.fen()
                G.add_edge(node, next_fen)
                
                move_score = get_move_quality_score(current_board, move)
                new_path_score = path_score + move_score
                
                build_graph(next_fen, current_board.copy(), current_depth - 1, new_path_score)
                current_board.pop()
        
        start_node = board.fen()
        build_graph(start_node, board.copy(), depth)
        
        if not G.successors(start_node):
            return None
        
        scores = {}
        for node in G.successors(start_node):
            successors = list(G.successors(node))
            connectivity_score = len(successors) ** 0.5
            
            avg_future_score = 0
            if successors:
                future_scores = [position_scores.get(succ, 0) for succ in successors]
                avg_future_score = np.mean(future_scores)
            
            total_score = connectivity_score + avg_future_score * 0.1
            scores[node] = total_score
        
        if not scores:
            return None
        
        best_fen = max(scores, key=scores.get)
        best_move = None
        
        for move in board.legal_moves:
            board.push(move)
            if board.fen() == best_fen:
                best_move = move
                break
            board.pop()
        
        return best_move
    
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
        board_copy = board.copy()
        board_copy.push(move)
        
        amplitude = 0
        future_positions = 0
        
        def explore_future(board_state, current_depth):
            nonlocal amplitude, future_positions
            
            if current_depth == 0:
                future_positions += 1
                position_quality = self.evaluate_position_quality(board_state)
                amplitude += position_quality * (0.8 ** (self.max_depth - current_depth))
                return
            
            legal_moves = list(board_state.legal_moves)
            if not legal_moves:
                future_positions += 1
                return
            
            for future_move in legal_moves[:self.max_breadth]:
                board_state.push(future_move)
                explore_future(board_state.copy(), current_depth - 1)
                board_state.pop()
        
        explore_future(board_copy, depth)
        
        if future_positions > 0:
            return amplitude / (future_positions ** 0.5)
        return amplitude
    
    def select_best_move_quantum_walk(self, board, legal_moves):
        if not legal_moves:
            return None
        
        if len(legal_moves) == 1:
            return legal_moves[0]
        
        best_move = None
        best_score = float('-inf')
        
        for move in legal_moves:
            score = self.quantum_amplitude_score(board, move, self.max_depth)
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move 