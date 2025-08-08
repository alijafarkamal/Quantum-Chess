import chess
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quantum.quantum_walk import evaluate_position_with_true_qwalk, run_true_quantum_walk, generate_move_graph
from quantum.grover_move_selector import true_quantum_walk_selector

def test_true_quantum_walk():
    print("Testing True Quantum Walk Implementation")
    print("=" * 50)
    
    # Test with starting position
    board = chess.Board()
    print(f"Testing with starting position: {board.fen()}")
    
    # Test graph generation
    print("\n1. Testing graph generation...")
    try:
        adj_list, fen_to_idx, idx_to_fen, move_tree = generate_move_graph(board, depth=2)
        print(f"✅ Graph generated successfully")
        print(f"   - Number of nodes: {len(adj_list)}")
        print(f"   - Number of FEN mappings: {len(fen_to_idx)}")
    except Exception as e:
        print(f"❌ Graph generation failed: {e}")
        return False
    
    # Test quantum walk execution
    print("\n2. Testing quantum walk execution...")
    try:
        start_idx = fen_to_idx.get(board.fen(), 0)
        final_counts = run_true_quantum_walk(adj_list, start_idx, steps=2)
        print(f"✅ Quantum walk executed successfully")
        print(f"   - Number of final states: {len(final_counts)}")
        if final_counts:
            print(f"   - Sample counts: {dict(list(final_counts.items())[:3])}")
    except Exception as e:
        print(f"❌ Quantum walk execution failed: {e}")
        return False
    
    # Test position evaluation
    print("\n3. Testing position evaluation...")
    try:
        move_scores = evaluate_position_with_true_qwalk(board, depth=2)
        print(f"✅ Position evaluation successful")
        print(f"   - Number of moves evaluated: {len(move_scores)}")
        if move_scores:
            print(f"   - Sample scores: {dict(list(move_scores.items())[:3])}")
    except Exception as e:
        print(f"❌ Position evaluation failed: {e}")
        return False
    
    # Test move selector
    print("\n4. Testing move selector...")
    try:
        legal_moves = list(board.legal_moves)
        result = true_quantum_walk_selector(board, legal_moves)
        if isinstance(result, tuple):
            best_move, prob_map = result
        else:
            best_move = result
            prob_map = {}
        
        print(f"✅ Move selector successful")
        if best_move:
            print(f"   - Best move: {board.san(best_move)}")
            print(f"   - Probability map: {prob_map}")
    except Exception as e:
        print(f"❌ Move selector failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✅ All tests passed! True quantum walk implementation is working.")
    return True

if __name__ == "__main__":
    test_true_quantum_walk() 