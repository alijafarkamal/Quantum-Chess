import chess
import networkx as nx

def get_board_from_fen(fen_string):
    try:
        board = chess.Board(fen_string)
        return board
    except ValueError as e:
        raise ValueError(f"Invalid FEN string: {e}")

def apply_move_to_board(board, move):
    new_board = board.copy()
    new_board.push(move)
    return new_board

def get_fen_from_board(board):
    return board.fen()

def is_valid_fen(fen_string):
    try:
        chess.Board(fen_string)
        return True
    except ValueError:
        return False

def get_board_info(board):
    info = {
        'turn': 'White' if board.turn else 'Black',
        'castling_rights': str(board.castling_rights),
        'en_passant': str(board.ep_square) if board.ep_square else 'None',
        'halfmove_clock': board.halfmove_clock,
        'fullmove_number': board.fullmove_number,
        'legal_moves_count': len(list(board.legal_moves)),
        'is_check': board.is_check(),
        'is_checkmate': board.is_checkmate(),
        'is_stalemate': board.is_stalemate(),
        'is_insufficient_material': board.is_insufficient_material()
    }
    return info

def generate_move_graph(board, depth=2):
    """
    Generate a graph of future board positions for quantum walk.
    Returns adjacency list, FEN mappings, and move tree.
    """
    G = nx.DiGraph()
    fen_to_idx = {}
    idx_to_fen = {}
    move_tree = {}
    node_counter = 0
    
    def add_node(fen):
        nonlocal node_counter
        if fen not in fen_to_idx:
            fen_to_idx[fen] = node_counter
            idx_to_fen[node_counter] = fen
            node_counter += 1
        return fen_to_idx[fen]
    
    def build_graph(current_board, current_depth, parent_move=None):
        current_fen = current_board.fen()
        current_idx = add_node(current_fen)
        
        if current_depth == 0:
            return current_idx
        
        legal_moves = list(current_board.legal_moves)
        if not legal_moves:
            return current_idx
        
        children = []
        for move in legal_moves:
            current_board.push(move)
            child_fen = current_board.fen()
            child_idx = add_node(child_fen)
            
            G.add_edge(current_idx, child_idx)
            children.append((move, child_idx))
            
            if current_depth > 1:
                build_graph(current_board, current_depth - 1, move)
            
            current_board.pop()
        
        if parent_move is not None:
            move_tree[parent_move.uci()] = children
        
        return current_idx
    
    start_idx = build_graph(board.copy(), depth)
    
    adj_list = {}
    for node in G.nodes():
        adj_list[node] = list(G.successors(node))
    
    return adj_list, fen_to_idx, idx_to_fen, move_tree 