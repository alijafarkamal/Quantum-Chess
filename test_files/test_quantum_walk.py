import chess
from chess_logic.move_eval import get_move_quality_score
from chess_logic.board_utils import get_board_from_fen, apply_move_to_board
from quantum.grover_move_selector import quantum_move_selector

def test_quantum_methods():
    print("♟️ Quantum Move Predictor - Method Comparison")
    print("=" * 60)
    
    test_positions = [
        ("Starting Position", "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"),
        ("Scholar's Mate Setup", "rnbqkbnr/pppp1ppp/8/4p3/5Q2/8/PPPP1PPP/RNB1KBNR b KQkq - 3 3"),
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
                walk_move = quantum_move_selector(board, legal_moves, "quantum_walk")
                walk_score = get_move_quality_score(board, walk_move) if walk_move else 0
                
                # Test Grover method
                grover_move = quantum_move_selector(board, legal_moves, "grover")
                grover_score = get_move_quality_score(board, grover_move) if grover_move else 0
                
                print(f"🔬 Quantum Walk: {board.san(walk_move)} (score: {walk_score})")
                print(f"⚛️ Quantum Grover: {board.san(grover_move)} (score: {grover_score})")
                
                if walk_move != grover_move:
                    print("⚠️ Methods chose different moves!")
                else:
                    print("✅ Both methods agreed!")
                    
            else:
                print("❌ No legal moves available")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n🎉 Method comparison completed!")

if __name__ == "__main__":
    test_quantum_methods() 