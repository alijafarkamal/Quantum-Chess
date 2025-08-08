import streamlit as st
import chess
import chess.svg
from io import BytesIO
import base64
from chess_logic.move_eval import evaluate_move
from chess_logic.board_utils import get_board_from_fen, apply_move_to_board
from quantum.grover_move_selector import quantum_move_selector

st.set_page_config(
    page_title="Quantum Chess",
    page_icon="♟️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* Global Lichess-style background */
    .stApp {
        background-color: #f0f0f0;
        color: #333333;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #759900 0%, #88aa00 100%);
        padding: 2rem 3rem;
        border-radius: 8px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 2.8rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    .board-container {
        background: white;
        padding: 1.5rem;
        border-radius: 6px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border: 1px solid #d4d4d4;
    }
    
    .fen-input {
        background: white;
        padding: 1.5rem;
        border-radius: 6px;
        border: 1px solid #d4d4d4;
        color: #333;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .status-card {
        background: linear-gradient(135deg, #759900 0%, #88aa00 100%);
        color: white;
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        font-weight: 500;
    }
    
    .fen-display {
        background: #f8f8f8;
        padding: 0.8rem;
        border-radius: 4px;
        border: 1px solid #e0e0e0;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        margin: 0.5rem 0;
        color: #666;
    }
    
    /* Lichess-style game status */
    .game-status {
        background: white;
        padding: 1rem;
        border-radius: 6px;
        border: 1px solid #d4d4d4;
        margin: 1rem 0;
        text-align: center;
        font-weight: 600;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Override Streamlit styling for Lichess look */
    .stTextInput > div > div > input {
        background-color: white !important;
        color: #333 !important;
        border: 1px solid #d4d4d4 !important;
        border-radius: 4px !important;
        font-size: 14px !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #759900 !important;
        box-shadow: 0 0 0 2px rgba(117, 153, 0, 0.2) !important;
    }
    
    .stSelectbox > div > div > select {
        background-color: white !important;
        color: #333 !important;
        border: 1px solid #d4d4d4 !important;
        border-radius: 4px !important;
    }
    
    .stTextArea > div > div > textarea {
        background-color: #f8f8f8 !important;
        color: #666 !important;
        border: 1px solid #e0e0e0 !important;
        font-family: 'Courier New', monospace !important;
        border-radius: 4px !important;
    }
    
    /* Clean alert styling */
    .stSuccess {
        background-color: #d4edda !important;
        border: 1px solid #c3e6cb !important;
        color: #155724 !important;
        border-radius: 4px !important;
    }
    
    .stError {
        background-color: #f8d7da !important;
        border: 1px solid #f5c6cb !important;
        color: #721c24 !important;
        border-radius: 4px !important;
    }
    
    .stWarning {
        background-color: #fff3cd !important;
        border: 1px solid #ffeaa7 !important;
        color: #856404 !important;
        border-radius: 4px !important;
    }
    
    .stInfo {
        background-color: #d1ecf1 !important;
        border: 1px solid #bee5eb !important;
        color: #0c5460 !important;
        border-radius: 4px !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'mode' not in st.session_state:
    st.session_state.mode = "menu"
if 'game_board' not in st.session_state:
    st.session_state.game_board = None
if 'game_history' not in st.session_state:
    st.session_state.game_history = []
if 'current_board' not in st.session_state:
    st.session_state.current_board = None
if 'original_board' not in st.session_state:
    st.session_state.original_board = None
if 'move_history' not in st.session_state:
    st.session_state.move_history = []
if 'fen_validated' not in st.session_state:
    st.session_state.fen_validated = False
if 'original_fen' not in st.session_state:
    st.session_state.original_fen = ""
if 'new_fen' not in st.session_state:
    st.session_state.new_fen = ""
if 'show_fens' not in st.session_state:
    st.session_state.show_fens = False



if st.session_state.mode == "menu":
    st.markdown("""
    <div class="main-header">
        <h1>♟️ Quantum Chess</h1>
        <p style="font-size: 1.2rem; margin-bottom: 0; opacity: 0.9;"><em>Classic chess meets quantum computing</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    st.markdown("""
    <style>
    .lichess-buttons .stButton > button {
        background: linear-gradient(135deg, #759900 0%, #88aa00 100%) !important;
        color: white !important;
        padding: 2.5rem 1.5rem !important;
        border-radius: 6px !important;
        border: none !important;
        font-size: 1.4rem !important;
        font-weight: 600 !important;
        margin: 0.5rem 0 !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
        text-align: center !important;
        width: 100% !important;
        height: 120px !important;
        letter-spacing: 0.5px !important;
    }
    
    .lichess-buttons .stButton > button:hover {
        background: linear-gradient(135deg, #88aa00 0%, #9bc500 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }
    
    .lichess-buttons .stButton > button:active {
        transform: translateY(0px) !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="lichess-buttons">', unsafe_allow_html=True)
        
        with col1:
            if st.button("♟️ Play Game", use_container_width=True, key="play_button"):
                st.session_state.mode = "play"
                st.session_state.game_board = chess.Board()
                st.session_state.game_history = []
                st.rerun()
        
        with col2:
            if st.button("🔬 Move Analysis", use_container_width=True, key="predictor_button"):
                st.session_state.mode = "predictor"
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.mode == "play":
    st.markdown('<h3 style="color: #333; text-align: center; font-weight: 600;">🎮 Playing vs Quantum AI</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <style>
    .game-controls .stButton > button {
        background: white !important;
        color: #333 !important;
        border: 1px solid #d4d4d4 !important;
        border-radius: 4px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        font-size: 14px !important;
    }
    
    .game-controls .stButton > button:hover {
        background: #f8f8f8 !important;
        border-color: #759900 !important;
        color: #759900 !important;
    }
    
    .compact-input .stTextInput > div > div > input {
        height: 40px !important;
        padding: 0.5rem !important;
        font-size: 14px !important;
    }
    
    .compact-button .stButton > button {
        background: linear-gradient(135deg, #759900 0%, #88aa00 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.2s ease !important;
        height: 40px !important;
        width: 100px !important;
    }
    
    .compact-button .stButton > button:hover {
        background: linear-gradient(135deg, #88aa00 0%, #9bc500 100%) !important;
        transform: translateY(-1px) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if st.button("← Back to Menu", help="Return to main menu"):
        st.session_state.mode = "menu"
        st.rerun()
    
    col_new, col_resign = st.columns(2)
    with col_new:
        if st.button("🔄 New Game", use_container_width=True):
            st.session_state.game_board = chess.Board()
            st.session_state.game_history = []
            if hasattr(st.session_state, 'resigned'):
                delattr(st.session_state, 'resigned')
            if hasattr(st.session_state, 'winner'):
                delattr(st.session_state, 'winner')
            st.rerun()
    
    with col_resign:
        if st.button("🏳️ Resign", use_container_width=True):
            st.session_state.resigned = True
            st.session_state.winner = "Black"
            st.rerun()
    
    if st.session_state.game_board:
        board = st.session_state.game_board
        
        if hasattr(st.session_state, 'resigned') and st.session_state.resigned:
            winner = st.session_state.get('winner', 'Black')
            loser = "White" if winner == "Black" else "Black"
            st.markdown(f"""
            <div style="background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; 
                        padding: 1.5rem; border-radius: 6px; text-align: center; font-weight: 600; margin: 1rem 0;">
                🏳️ <strong>GAME OVER</strong><br>
                <span style="font-size: 1.1em;">{winner} wins by resignation</span><br>
                <small style="opacity: 0.8;">{loser} resigned</small>
            </div>
            """, unsafe_allow_html=True)
        elif board.is_checkmate():
            winner = "Black" if board.turn else "White"
            loser = "White" if board.turn else "Black"
            st.markdown(f"""
            <div style="background: #d4edda; border: 1px solid #c3e6cb; color: #155724; 
                        padding: 1.5rem; border-radius: 6px; text-align: center; font-weight: 600; margin: 1rem 0;">
                🏆 <strong>CHECKMATE!</strong><br>
                <span style="font-size: 1.1em;">{winner} wins by checkmate</span><br>
                <small style="opacity: 0.8;">{loser} is checkmated</small>
            </div>
            """, unsafe_allow_html=True)
        elif board.is_stalemate():
            st.markdown("""
            <div style="background: #fff3cd; border: 1px solid #ffeaa7; color: #856404; 
                        padding: 1.5rem; border-radius: 6px; text-align: center; font-weight: 600; margin: 1rem 0;">
                🤝 <strong>STALEMATE!</strong><br>
                <span style="font-size: 1.1em;">Game ends in a draw</span><br>
                <small style="opacity: 0.8;">No legal moves available</small>
            </div>
            """, unsafe_allow_html=True)
        elif board.is_insufficient_material():
            st.markdown("""
            <div style="background: #fff3cd; border: 1px solid #ffeaa7; color: #856404; 
                        padding: 1.5rem; border-radius: 6px; text-align: center; font-weight: 600; margin: 1rem 0;">
                🤝 <strong>DRAW!</strong><br>
                <span style="font-size: 1.1em;">Insufficient material</span><br>
                <small style="opacity: 0.8;">Neither side can checkmate</small>
            </div>
            """, unsafe_allow_html=True)
        elif board.is_seventyfive_moves():
            st.markdown("""
            <div style="background: #fff3cd; border: 1px solid #ffeaa7; color: #856404; 
                        padding: 1.5rem; border-radius: 6px; text-align: center; font-weight: 600; margin: 1rem 0;">
                🤝 <strong>DRAW!</strong><br>
                <span style="font-size: 1.1em;">75-move rule</span><br>
                <small style="opacity: 0.8;">Too many moves without progress</small>
            </div>
            """, unsafe_allow_html=True)
        elif board.is_fivefold_repetition():
            st.markdown("""
            <div style="background: #fff3cd; border: 1px solid #ffeaa7; color: #856404; 
                        padding: 1.5rem; border-radius: 6px; text-align: center; font-weight: 600; margin: 1rem 0;">
                🤝 <strong>DRAW!</strong><br>
                <span style="font-size: 1.1em;">Fivefold repetition</span><br>
                <small style="opacity: 0.8;">Position repeated 5 times</small>
            </div>
            """, unsafe_allow_html=True)
        elif board.is_check():
            st.markdown("""
            <div style="background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; 
                        padding: 1rem; border-radius: 4px; text-align: center; font-weight: 600; margin: 1rem 0;">
                ♔ CHECK!
            </div>
            """, unsafe_allow_html=True)
        
        col_left, col_center, col_right = st.columns([1, 2, 1])
        
        with col_left:
            turn_text = "White to move" if board.turn else "Black (AI) to move"
            turn_color = "#759900" if board.turn else "#666"
            st.markdown(f"""
            <div style="background: white; padding: 1rem; border-radius: 6px; border: 1px solid #d4d4d4; 
                        text-align: center; font-weight: 600; margin-bottom: 1rem; color: {turn_color};">
                {turn_text}
            </div>
            """, unsafe_allow_html=True)
            
            if board.turn and not board.is_game_over():
                st.markdown("**Enter Your Move:**")
                
                with st.form(key="move_form"):
                    move_input = st.text_input(
                        "Move", 
                        placeholder="e.g., e4, Nf3, O-O",
                        label_visibility="collapsed"
                    )
                    submitted = st.form_submit_button("Make Move", use_container_width=True)
                    
                    if submitted and move_input.strip():
                        try:
                            move = board.parse_san(move_input.strip())
                            board.push(move)
                            st.session_state.game_history.append(f"White: {move_input.strip()}")
                            st.success(f"Move played: {move_input.strip()}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Invalid move: {e}")
                    elif submitted:
                        st.warning("Please enter a move!")
            
            elif not board.turn and not board.is_game_over():
                st.markdown("""
                <div style="background: #f8f8f8; padding: 1rem; border-radius: 6px; border: 1px solid #d4d4d4; 
                            text-align: center; color: #666; margin: 1rem 0;">
                    🤖 AI is thinking...
                </div>
                """, unsafe_allow_html=True)
                
                with st.spinner("Quantum AI analyzing..."):
                    legal_moves = list(board.legal_moves)
                    if legal_moves:
                        result = quantum_move_selector(board, legal_moves, "true_quantum_walk")
                        if isinstance(result, tuple):
                            ai_move, prob_map = result
                        else:
                            ai_move = result
                            prob_map = {}
                        
                        if ai_move:
                            move_san = board.san(ai_move)
                            board.push(ai_move)
                            st.session_state.game_history.append(f"Black: {move_san}")
                            st.success(f"AI plays: {move_san}")
                            st.rerun()
        
        with col_center:
            st.markdown('<div class="board-container">', unsafe_allow_html=True)
            
            board_svg = chess.svg.board(
                board=board, 
                size=550,
                style="""
                .square.light { fill: #f0d9b5 !important; }
                .square.dark { fill: #b58863 !important; }
                .square.light.highlight { fill: #cdd26a !important; }
                .square.dark.highlight { fill: #aaa23a !important; }
                """
            )
            st.markdown(f'<div style="text-align: center;">{board_svg}</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_right:
            st.markdown("**Game History**")
            
            if st.session_state.game_history:
                st.markdown("""
                <div style="background: white; padding: 1rem; border-radius: 6px; 
                            border: 1px solid #d4d4d4; max-height: 400px; overflow-y: auto;">
                """, unsafe_allow_html=True)
                
                for i, move in enumerate(st.session_state.game_history, 1):
                    if "White:" in move:
                        st.markdown(f"**{i}.** {move.replace('White: ', '')}")
                    else:
                        st.markdown(f"**{i}.** {move.replace('Black: ', '')} *(AI)*")
                
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: #f8f8f8; padding: 1rem; border-radius: 6px; 
                            border: 1px solid #e0e0e0; text-align: center; color: #666;">
                    No moves yet
                </div>
                """, unsafe_allow_html=True)

elif st.session_state.mode == "predictor":
    st.markdown('<h3 style="color: #333; text-align: center; font-weight: 600;">🔬 Position Analysis</h3>', unsafe_allow_html=True)
    
    # Clean back button
    if st.button("← Back to Menu", help="Return to main menu"):
        st.session_state.mode = "menu"
        st.rerun()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎯 Chess Position Setup")
        
        # FEN Input Section
        with st.container():
            st.markdown('<div class="fen-input">', unsafe_allow_html=True)
            
            fen_input = st.text_input(
                "📋 Enter FEN String (Required)",
                value="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                help="Enter a valid FEN string to set up the position",
                key="fen_input"
            )
            
            col_submit, col_reset = st.columns(2)
            
            with col_submit:
                if st.button("✅ Validate FEN", type="primary", use_container_width=True):
                    try:
                        board = get_board_from_fen(fen_input)
                        st.session_state.current_board = board
                        st.session_state.original_board = board.copy()
                        st.session_state.fen_validated = True
                        st.session_state.original_fen = ""
                        st.session_state.new_fen = ""
                        st.session_state.show_fens = False
                        st.success("✅ FEN string validated successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Invalid FEN string: {e}")
                        st.session_state.fen_validated = False
            
            with col_reset:
                if st.button("🔄 Reset Position", use_container_width=True):
                    st.session_state.current_board = None
                    st.session_state.original_board = None
                    st.session_state.fen_validated = False
                    st.session_state.move_history = []
                    st.session_state.original_fen = ""
                    st.session_state.new_fen = ""
                    st.session_state.show_fens = False
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Board Display and Analysis
        if st.session_state.fen_validated and st.session_state.current_board:
            board = st.session_state.current_board
            legal_moves = list(board.legal_moves)
            
            st.markdown('<div class="status-card">', unsafe_allow_html=True)
            st.markdown(f"📊 **{len(legal_moves)} legal moves** available")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Algorithm Selection
            col_method, col_button = st.columns([1, 2])
            
            with col_method:
                method = st.selectbox(
                    "🎯 Algorithm Method",
                    ["QAOA (Optimization)", "True Quantum Walk (Qiskit)", "Quantum Walk (Intelligent)", "Quantum Grover (Classic)"],
                    help="QAOA frames move selection as optimization, True Quantum Walk uses genuine Qiskit circuits, Quantum Walk explores future positions, while Grover uses immediate evaluation"
                )
            
            with col_button:
                if st.button("🚀 Run Quantum Move Predictor", type="primary", use_container_width=True):
                    if len(legal_moves) == 0:
                        st.warning("⚠️ No legal moves available!")
                    else:
                        with st.spinner("🔬 Quantum algorithm analyzing moves..."):
                            try:
                                if "QAOA" in method:
                                    method_type = "qaoa"
                                elif "True Quantum Walk" in method:
                                    method_type = "true_quantum_walk"
                                elif "Walk" in method:
                                    method_type = "quantum_walk"
                                else:
                                    method_type = "grover"
                                result = quantum_move_selector(board, legal_moves, method_type)
                                
                                if isinstance(result, tuple):
                                    best_move, prob_map = result
                                else:
                                    best_move = result
                                    prob_map = {}
                                
                                if best_move:
                                    st.success(f"🎯 **Quantum algorithm selected:** {board.san(best_move)}")
                                    
                                    # Display quantum probabilities
                                    if prob_map:
                                        st.markdown("### 🔢 Quantum Sampling Results")
                                        import pandas as pd
                                        rows = []
                                        for uci, p in prob_map.items():
                                            move_obj = chess.Move.from_uci(uci)
                                            san_move = board.san(move_obj)
                                            rows.append({"Move": san_move, "UCI": uci, "Probability": f"{p:.3f}"})
                                        df = pd.DataFrame(rows).sort_values('Probability', ascending=False)
                                        st.table(df)
                                        
                                        # Bar chart
                                        prob_data = pd.DataFrame(rows)
                                        prob_data['Probability'] = prob_data['Probability'].astype(float)
                                        st.bar_chart(prob_data.set_index('Move')['Probability'])
                                    
                                    new_board = apply_move_to_board(board, best_move)
                                    
                                    # Store the new board and FENs in session state
                                    st.session_state.current_board = new_board
                                    st.session_state.original_fen = board.fen()
                                    st.session_state.new_fen = new_board.fen()
                                    st.session_state.show_fens = True
                                    
                                    # Track move history
                                    move_entry = {
                                        'move': board.san(best_move),
                                        'move_uci': best_move.uci(),
                                        'from_fen': board.fen(),
                                        'to_fen': new_board.fen(),
                                        'method': method
                                    }
                                    st.session_state.move_history.append(move_entry)
                                    
                                    st.rerun()
                                    
                            except Exception as e:
                                st.error(f"❌ Error in quantum algorithm: {e}")
        
        # Display boards if we have results
        if st.session_state.show_fens and st.session_state.original_fen and st.session_state.new_fen:
            # Recreate boards from FENs
            original_board = get_board_from_fen(st.session_state.original_fen)
            new_board = get_board_from_fen(st.session_state.new_fen)
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown('<div class="board-container">', unsafe_allow_html=True)
                st.markdown("### 📋 Original Position")
                original_svg = chess.svg.board(board=original_board, size=400)
                st.markdown(f'<div style="text-align: center;">{original_svg}</div>', unsafe_allow_html=True)
                
                # Display FEN for original board
                st.markdown('<div class="fen-display">', unsafe_allow_html=True)
                st.text_area("Original FEN:", value=st.session_state.original_fen, height=60, key="original_fen_display")
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col_b:
                st.markdown('<div class="board-container">', unsafe_allow_html=True)
                st.markdown("### ⚛️ After Quantum Move")
                new_svg = chess.svg.board(board=new_board, size=400)
                st.markdown(f'<div style="text-align: center;">{new_svg}</div>', unsafe_allow_html=True)
                
                # Display FEN for new board
                st.markdown('<div class="fen-display">', unsafe_allow_html=True)
                st.text_area("New Position FEN:", value=st.session_state.new_fen, height=60, key="new_fen_display")
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Move information
            move_info = f"**Move played:** {st.session_state.move_history[-1]['move']}"
            if new_board.is_check():
                move_info += " ♔ **Check!**"
            elif new_board.is_checkmate():
                move_info += " ♔ **Checkmate!**"
            
            st.info(move_info)
            
            # Continue playing option
            if st.button("🎯 Continue from New Position", type="secondary"):
                st.session_state.original_board = original_board
                st.session_state.show_fens = False
                st.rerun()
        
        # Show move history
        if st.session_state.move_history:
            st.markdown("### 📜 Move History")
            for i, entry in enumerate(st.session_state.move_history[-5:], 1):
                st.write(f"{i}. **{entry['move']}** ({entry['method']})")
            
            if st.button("🗑️ Clear History"):
                st.session_state.move_history = []
                st.session_state.show_fens = False
                st.session_state.original_fen = ""
                st.session_state.new_fen = ""
                st.rerun()

    with col2:
        st.markdown("### 📊 Game Status")
        
        if st.session_state.fen_validated and st.session_state.current_board:
            board = st.session_state.current_board
            turn_color = "🟢 White" if board.turn else "⚫ Black"
            st.markdown(f"**Turn:** {turn_color}")
            
            if board.is_check():
                st.warning("♔ **King in Check!**")
            elif board.is_checkmate():
                st.error("♔ **Checkmate!**")
            elif board.is_stalemate():
                st.warning("♔ **Stalemate!**")
            elif board.is_insufficient_material():
                st.info("♔ **Insufficient Material**")
        
        with st.expander("🔧 Technical Details"):
            if st.session_state.fen_validated and st.session_state.current_board:
                board = st.session_state.current_board
                castling_rights = []
                if board.has_kingside_castling_rights(chess.WHITE):
                    castling_rights.append("White Kingside")
                if board.has_queenside_castling_rights(chess.WHITE):
                    castling_rights.append("White Queenside")
                if board.has_kingside_castling_rights(chess.BLACK):
                    castling_rights.append("Black Kingside")
                if board.has_queenside_castling_rights(chess.BLACK):
                    castling_rights.append("Black Queenside")
                
                castling_text = ", ".join(castling_rights) if castling_rights else "None"
                st.write(f"**Castling Rights:** {castling_text}")
                
                en_passant_square = chess.square_name(board.ep_square) if board.ep_square else "None"
                st.write(f"**En Passant:** {en_passant_square}")
                st.write(f"**Halfmove Clock:** {board.halfmove_clock}")
                st.write(f"**Fullmove Number:** {board.fullmove_number}")
        
        st.markdown("---")
        
        st.markdown("### ⚛️ Quantum Algorithm")
        st.markdown("""
        This app uses **quantum-inspired amplitude amplification** to find the optimal chess move:
        
        1. **Generate** all legal moves
        2. **Evaluate** each move using material scoring  
        3. **Apply** amplitude amplification to enhance best moves
        4. **Return** the quantum-inspired decision
        """)

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1.5rem; background: white; 
            border-radius: 6px; margin-top: 2rem; border: 1px solid #d4d4d4;">
    <p style="color: #666; font-size: 14px; margin: 0;">
        <em>⚛️ Built for CQHack25 - Quantum Chess Experience</em>
    </p>
</div>
""", unsafe_allow_html=True) 