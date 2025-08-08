import chess
from chess_logic.move_eval import get_move_quality_score
from chess_logic.board_utils import get_board_from_fen, apply_move_to_board
from quantum.grover_move_selector import quantum_move_selector

def demo_play_game():
    print("🎮 Demo: Play with Quantum Computer")
    print("=" * 50)
    
    board = chess.Board()
    game_history = []
    
    # Simulate a game
    moves = ["e4", "e5", "Nf3", "Nc6", "Bb5", "a6"]
    
    for i, move in enumerate(moves):
        if i % 2 == 0:  # User move (White)
            print(f"👤 User plays: {move}")
            game_history.append(f"White: {move}")
        else:  # Quantum AI move (Black)
            print(f"⚛️ Quantum AI plays: {move}")
            game_history.append(f"Black: {move}")
        
        # Apply move
        move_obj = board.parse_san(move)
        board.push(move_obj)
        
        # Show position
        print(f"Position after move {i+1}: {board.fen()}")
        
        if board.is_check():
            print("♔ Check!")
        elif board.is_checkmate():
            print("♔ Checkmate!")
            break
    
    print("\n📜 Game History:")
    for i, move in enumerate(game_history, 1):
        print(f"{i}. {move}")
    
    print("\n🎉 Game demo completed!")

def demo_predictor():
    print("\n🔬 Demo: Quantum Move Predictor")
    print("=" * 50)
    
    test_positions = [
        ("Starting Position", "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"),
        ("Tactical Position", "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4")
    ]
    
    for name, fen in test_positions:
        print(f"\n🎯 Analyzing: {name}")
        print(f"FEN: {fen}")
        
        try:
            board = get_board_from_fen(fen)
            legal_moves = list(board.legal_moves)
            
            print(f"Legal moves: {len(legal_moves)}")
            
            if legal_moves:
                result = quantum_move_selector(board, legal_moves, "quantum_walk")
                if isinstance(result, tuple):
                    best_move, prob_map = result
                else:
                    best_move = result
                    prob_map = {}
                
                print(f"🎯 Quantum algorithm selected: {board.san(best_move)}")
                
                if prob_map:
                    print("📊 Top move probabilities:")
                    for uci, prob in sorted(prob_map.items(), key=lambda x: x[1], reverse=True)[:3]:
                        move_obj = chess.Move.from_uci(uci)
                        san_move = board.san(move_obj)
                        print(f"   {san_move}: {prob:.3f}")
                
                # Show resulting position
                new_board = apply_move_to_board(board, best_move)
                print(f"📋 New FEN: {new_board.fen()}")
                
            else:
                print("❌ No legal moves available")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n🎉 Predictor demo completed!")

def main():
    print("♟️ Quantum Chess - Dual Mode Demo")
    print("=" * 60)
    
    print("\nThis demo shows the two main modes:")
    print("1. 🎮 Play with Quantum Computer - Real game vs quantum AI")
    print("2. 🔬 Quantum Move Predictor - Position analysis tool")
    
    demo_play_game()
    demo_predictor()
    
    print("\n💡 In the web app:")
    print("   - Click '♟️ Play with Quantum Computer' for real games")
    print("   - Click '🔬 Quantum Move Predictor' for position analysis")
    print("   - Both modes use genuine quantum algorithms!")

if __name__ == "__main__":
    main() 