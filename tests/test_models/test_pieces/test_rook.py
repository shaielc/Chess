from models.pieces.piece import PiecesContainer
from models.pieces.rook import Rook


def test_rook_moves():
    rook = Rook(4,4)
    moves = rook.valid_moves(PiecesContainer([]))
    assert(len(moves) == 14)
    assert(all([(i,4) in moves for i in range(8) if i != 4]))
    assert(all([(4,i) in moves for i in range(8) if i != 4]))


def test_rook_blocked_ally():
    rook = Rook(4,4)
    ally_piece = Rook(6,4)
    enemy_piece = Rook(4,6, white=False)
    moves = rook.valid_moves(PiecesContainer([ally_piece]))
    assert(len(moves) == 12)
    assert((0,4) in moves)
    assert((5,4) in moves)
    assert((6,4) not in moves)
    assert((7,4) not in moves)
    assert(all([(4,i) in moves for i in range(8) if i != 4]))

def test_rook_blocked_enemy():
    rook = Rook(4,4)
    enemy_piece = Rook(4,6, white=False)
    moves = rook.valid_moves(PiecesContainer([enemy_piece]))
    assert(len(moves) == 13)
    assert((4,0) in moves)
    assert((4,6) in moves)
    assert((4,7) not in moves)
    assert(all([(i,4) in moves for i in range(8) if i != 4]))
    
    