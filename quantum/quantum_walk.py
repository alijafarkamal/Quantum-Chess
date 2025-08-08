import networkx as nx
import chess
import math
import copy

PIECE_VALUES = {chess.PAWN:1, chess.KNIGHT:3, chess.BISHOP:3, chess.ROOK:5, chess.QUEEN:9, chess.KING:0}

def material_value(board):
    val = 0
    for sq in chess.SQUARES:
        p = board.piece_at(sq)
        if p:
            v = PIECE_VALUES.get(p.piece_type, 0)
            val += v if p.color == board.turn else -v
    return val

def position_heuristic(board):
    mat = material_value(board)
    mobility = len(list(board.legal_moves))
    king_in_check = 1.0 if board.is_check() else 0.0
    score = mat + 0.01 * mobility - 0.5 * king_in_check
    return score

def build_subtree(board, depth):
    G = nx.DiGraph()
    start = board.fen()
    def rec(b, d):
        node = b.fen()
        if d == 0:
            return
        for mv in list(b.legal_moves):
            b.push(mv)
            child = b.fen()
            G.add_edge(node, child)
            rec(b, d-1)
            b.pop()
    rec(board.copy(), depth)
    return G

def quantum_walk_scores(board, depth=2):
    scores = {}
    base_board = board.copy()
    start = base_board.fen()
    G = build_subtree(base_board, depth)
    
    for mv in list(base_board.legal_moves):
        base_board.push(mv)
        node = base_board.fen()
        nodes = [node]
        
        for _ in range(depth-1):
            next_nodes = []
            for n in nodes:
                next_nodes.extend(list(G.successors(n)))
            nodes = next_nodes if next_nodes else nodes
        
        agg = 0.0
        count = 0
        for n in nodes:
            b = chess.Board(n)
            h = position_heuristic(b)
            deg = max(1, G.out_degree(n))
            agg += h * math.sqrt(deg)
            count += 1
        base_board.pop()
        scores[mv] = (agg / count) if count>0 else position_heuristic(chess.Board(node))
    
    return scores

def quick_prune(board, moves):
    pruned = []
    for m in moves:
        board.push(m)
        if board.is_check():
            board.pop()
            continue
        board.pop()
        pruned.append(m)
    return pruned 