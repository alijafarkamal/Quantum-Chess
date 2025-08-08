import numpy as np
import random
import chess
from chess_logic.move_eval import get_move_quality_score
from quantum.quantum_walk import quantum_walk_scores, quick_prune
from quantum.amplitude_selector import amplitude_sample

def quantum_move_selector(board, legal_moves, method_type='quantum_walk', top_k=8):
    legal = list(legal_moves)
    if len(legal) == 0:
        return None, {}

    if len(legal) == 1:
        return legal[0], {legal[0].uci(): 1.0}

    if method_type == 'quantum_walk':
        scores_map = quantum_walk_scores(board, depth=2)
        scores = [scores_map.get(m, 0.0) for m in legal]
    elif method_type == 'classical':
        scores = []
        for m in legal:
            board.push(m)
            s = 0
            for sq in board.piece_map().keys():
                p = board.piece_at(sq)
                if p:
                    s += {1:1,2:3,3:3,4:5,5:9,6:0}.get(p.piece_type,0) * (1 if p.color==board.turn else -1)
            scores.append(s)
            board.pop()
    else:
        scores = []
        for m in legal:
            score = get_move_quality_score(board, m)
            scores.append(score)

    if len(scores) <= 2:
        best_idx = int(np.argmax(scores))
        return legal[best_idx], {legal[best_idx].uci(): 1.0}

    idx_sorted = np.argsort(scores)[::-1]
    top_indices = idx_sorted[:min(top_k, len(scores))]
    top_scores = [scores[i] for i in top_indices]
    top_moves = [legal[i] for i in top_indices]

    try:
        probs, raw_counts = amplitude_sample(top_scores, shots=512)
        if not probs:
            best_idx_local = 0
        else:
            best_idx_local = max(probs, key=probs.get)
        chosen_move = top_moves[best_idx_local]
        prob_map = {top_moves[i].uci(): probs.get(i,0) for i in range(len(top_moves))}
        return chosen_move, prob_map
    except Exception as e:
        print(f"Quantum sampling failed, falling back to classical: {e}")
        best_idx = int(np.argmax(scores))
        return legal[best_idx], {legal[best_idx].uci(): 1.0}

def quantum_walk_selector(board, legal_moves):
    try:
        return quantum_move_selector(board, legal_moves, "quantum_walk")
    except Exception as e:
        print(f"Quantum walk failed, falling back to classical: {e}")
        return classical_fallback(board, legal_moves), {}

def quantum_grover_selector(board, legal_moves):
    try:
        return quantum_move_selector(board, legal_moves, "grover")
    except Exception as e:
        print(f"Quantum grover failed, falling back to classical: {e}")
        return classical_fallback(board, legal_moves), {}

def classical_fallback(board, legal_moves):
    if not legal_moves:
        return None
    
    best_move = None
    best_score = float('-inf')
    
    for move in legal_moves:
        score = get_move_quality_score(board, move)
        if score > best_score:
            best_score = score
            best_move = move
    
    return best_move 