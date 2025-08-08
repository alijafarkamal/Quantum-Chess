import chess
from chess_logic.move_eval import get_move_quality_score
from chess_logic.board_utils import get_board_from_fen, apply_move_to_board
from quantum.grover_move_selector import quantum_move_selector

def demo_continuation_features():
    print("♟️ Quantum Move Predictor - Continuation Demo")
    print("=" * 60)
    
    # Simulate a game continuation
    positions = [
        ("Starting Position", "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"),
        ("After e4", "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"),
        ("After e5", "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq e6 0 2"),
        ("After Nf3", "rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2")
    ]
    
    print("\n🎮 Simulating a game continuation:")
    
    for i, (name, fen) in enumerate(positions):
        print(f"\n📋 Position {i+1}: {name}")
        print(f"FEN: {fen}")
        
        try:
            board = get_board_from_fen(fen)
            legal_moves = list(board.legal_moves)
            
            print(f"Legal moves: {len(legal_moves)}")
            
            if legal_moves:
                # Test both methods
                walk_move = quantum_move_selector(board, legal_moves, "quantum_walk")
                grover_move = quantum_move_selector(board, legal_moves, "grover")
                
                print(f"🔬 Quantum Walk suggests: {board.san(walk_move)}")
                print(f"⚛️ Quantum Grover suggests: {board.san(grover_move)}")
                
                # Show the resulting position
                new_board = apply_move_to_board(board, walk_move)
                print(f"📊 New FEN: {new_board.fen()}")
                
                if new_board.is_check():
                    print("♔ Check!")
                elif new_board.is_checkmate():
                    print("♔ Checkmate!")
                    
            else:
                print("❌ No legal moves available")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n🎉 Continuation demo completed!")
    print("\n💡 In the web app, you can:")
    print("   - Continue playing from any position")
    print("   - Copy FEN strings for both positions")
    print("   - View move history")
    print("   - Reset to starting position")

if __name__ == "__main__":
    demo_continuation_features() 