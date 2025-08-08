import chess
from chess_logic.move_eval import get_move_quality_score
from chess_logic.board_utils import get_board_from_fen, apply_move_to_board
from quantum.grover_move_selector import quantum_move_selector

def test_quantum_enhanced():
    print("♟️ Quantum Move Predictor - Enhanced Quantum Test")
    print("=" * 60)
    
    test_positions = [
        ("Starting Position", "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"),
        ("Tactical Position", "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4"),
        ("Endgame", "8/8/8/8/8/8/4K3/4k3 w - - 0 1")
    ]
    
    for name, fen in test_positions:
        print(f"\n🎯 Testing: {name}")
        print(f"FEN: {fen}")
        
        try:
            board = get_board_from_fen(fen)
            legal_moves = list(board.legal_moves)
            
            print(f"Legal moves: {len(legal_moves)}")
            
            if legal_moves:
                # Test Quantum Walk method
                walk_result = quantum_move_selector(board, legal_moves, "quantum_walk")
                if isinstance(walk_result, tuple):
                    walk_move, walk_probs = walk_result
                else:
                    walk_move = walk_result
                    walk_probs = {}
                
                print(f"🔬 Quantum Walk: {board.san(walk_move)}")
                if walk_probs:
                    print("   Probabilities:")
                    for uci, prob in sorted(walk_probs.items(), key=lambda x: x[1], reverse=True)[:3]:
                        move_obj = chess.Move.from_uci(uci)
                        san_move = board.san(move_obj)
                        print(f"     {san_move}: {prob:.3f}")
                
                # Test Classical method
                classical_result = quantum_move_selector(board, legal_moves, "classical")
                if isinstance(classical_result, tuple):
                    classical_move, classical_probs = classical_result
                else:
                    classical_move = classical_result
                    classical_probs = {}
                
                print(f"⚛️ Classical: {board.san(classical_move)}")
                
                if walk_move != classical_move:
                    print("⚠️ Methods chose different moves!")
                else:
                    print("✅ Both methods agreed!")
                    
            else:
                print("❌ No legal moves available")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n🎉 Enhanced quantum test completed!")

if __name__ == "__main__":
    test_quantum_enhanced() 