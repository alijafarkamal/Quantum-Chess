import streamlit as st
import chess
import stchess

def test_interactive_chess():
    print("♟️ Testing Interactive Chessboard")
    print("=" * 40)
    
    # Test basic chess board
    board = chess.Board()
    fen = board.fen()
    
    print(f"✅ Board created: {fen}")
    print(f"✅ Legal moves: {len(list(board.legal_moves))}")
    
    # Test stchess import
    try:
        print("✅ stchess imported successfully")
    except Exception as e:
        print(f"❌ stchess import failed: {e}")
    
    # Test move validation
    test_move = chess.Move.from_uci("e2e4")
    if test_move in board.legal_moves:
        print("✅ Move validation working")
    else:
        print("❌ Move validation failed")
    
    print("🎉 Interactive chess test completed!")

if __name__ == "__main__":
    test_interactive_chess() 