import chess
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quantum.qaoa_move_selector import select_move_with_qaoa, qaoa_move_selector, evaluate_board_state
from quantum.grover_move_selector import qaoa_selector

def test_qaoa_move_selector():
    print("Testing QAOA Move Selector Implementation")
    print("=" * 50)
    
    # Test with starting position
    board = chess.Board()
    print(f"Testing with starting position: {board.fen()}")
    
    # Test board state evaluation
    print("\n1. Testing board state evaluation...")
    try:
        score = evaluate_board_state(board, board.turn)
        print(f"✅ Board state evaluation successful")
        print(f"   - Score: {score}")
    except Exception as e:
        print(f"❌ Board state evaluation failed: {e}")
        return False
    
    # Test QAOA move selection
    print("\n2. Testing QAOA move selection...")
    try:
        legal_moves = list(board.legal_moves)
        result = select_move_with_qaoa(board)
        if isinstance(result, tuple):
            best_move, prob_map = result
        else:
            best_move = result
            prob_map = {}
        
        print(f"✅ QAOA move selection successful")
        if best_move:
            print(f"   - Best move: {board.san(best_move)}")
            print(f"   - Probability map: {prob_map}")
    except Exception as e:
        print(f"❌ QAOA move selection failed: {e}")
        return False
    
    # Test QAOA selector wrapper
    print("\n3. Testing QAOA selector wrapper...")
    try:
        result = qaoa_selector(board, legal_moves)
        if isinstance(result, tuple):
            best_move, prob_map = result
        else:
            best_move = result
            prob_map = {}
        
        print(f"✅ QAOA selector wrapper successful")
        if best_move:
            print(f"   - Best move: {board.san(best_move)}")
            print(f"   - Probability map: {prob_map}")
    except Exception as e:
        print(f"❌ QAOA selector wrapper failed: {e}")
        return False
    
    # Test with a more complex position
    print("\n4. Testing with complex position...")
    try:
        complex_board = chess.Board("rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")
        print(f"Complex position: {complex_board.fen()}")
        
        result = select_move_with_qaoa(complex_board)
        if isinstance(result, tuple):
            best_move, prob_map = result
        else:
            best_move = result
            prob_map = {}
        
        print(f"✅ Complex position QAOA successful")
        if best_move:
            print(f"   - Best move: {complex_board.san(best_move)}")
            print(f"   - Probability map: {prob_map}")
    except Exception as e:
        print(f"❌ Complex position QAOA failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✅ All QAOA tests passed! QAOA implementation is working.")
    return True

if __name__ == "__main__":
    test_qaoa_move_selector() 