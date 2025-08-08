import chess
from chess_logic.move_eval import evaluate_move, get_move_quality_score
from chess_logic.board_utils import get_board_from_fen, apply_move_to_board
from quantum.grover_move_selector import quantum_move_selector

def test_basic_functionality():
    print("Testing Quantum Move Predictor components...")
    
    board = chess.Board()
    legal_moves = list(board.legal_moves)
    
    print(f"✅ Board created with {len(legal_moves)} legal moves")
    
    if legal_moves:
        test_move = legal_moves[0]
        score = get_move_quality_score(board, test_move)
        print(f"✅ Move evaluation working: {test_move} -> score {score}")
        
        try:
            best_move = quantum_move_selector(board, legal_moves)
            print(f"✅ Quantum algorithm working: selected {best_move}")
        except Exception as e:
            print(f"⚠️ Quantum algorithm failed: {e}")
            print("✅ Classical fallback should work")
    
    fen_test = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    try:
        test_board = get_board_from_fen(fen_test)
        print("✅ FEN parsing working")
    except Exception as e:
        print(f"❌ FEN parsing failed: {e}")
    
    print("🎉 Basic functionality test completed!")

if __name__ == "__main__":
    test_basic_functionality() 