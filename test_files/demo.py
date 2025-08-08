import chess
from chess_logic.move_eval import get_move_quality_score
from chess_logic.board_utils import get_board_from_fen, apply_move_to_board
from quantum.grover_move_selector import quantum_move_selector

def demo_quantum_chess():
    print("♟️ Quantum Move Predictor Demo")
    print("=" * 50)
    
    positions = [
        ("Starting Position", "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"),
        ("Scholar's Mate Setup", "rnbqkbnr/pppp1ppp/8/4p3/5Q2/8/PPPP1PPP/RNB1KBNR b KQkq - 3 3"),
        ("Endgame Position", "8/8/8/8/8/8/4K3/4k3 w - - 0 1"),
        ("Tactical Position", "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4")
    ]
    
    for name, fen in positions:
        print(f"\n🎯 Testing: {name}")
        print(f"FEN: {fen}")
        
        try:
            board = get_board_from_fen(fen)
            legal_moves = list(board.legal_moves)
            
            print(f"Legal moves: {len(legal_moves)}")
            
            if legal_moves:
                best_move = quantum_move_selector(board, legal_moves)
                if best_move:
                    print(f"🎯 Quantum algorithm selected: {board.san(best_move)}")
                    
                    new_board = apply_move_to_board(board, best_move)
                    print(f"New FEN: {new_board.fen()}")
                    
                    if new_board.is_check():
                        print("♔ Check!")
                    elif new_board.is_checkmate():
                        print("♔ Checkmate!")
                else:
                    print("❌ No move selected")
            else:
                print("❌ No legal moves available")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n🎉 Demo completed!")

if __name__ == "__main__":
    demo_quantum_chess() 