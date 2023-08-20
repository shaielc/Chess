from models.pieces.piece import PiecesContainer
from models.pieces.king import King

def test_king_moves():
    king = King(4,4)
    moves = king.valid_moves(PiecesContainer([]))

    assert(len(moves) == 8)
    assert((5,4) in moves)
    assert((5,5) in moves)
    assert((4,5) in moves)
    assert((3,5) in moves)
    assert((3,4) in moves)
    assert((3,3) in moves)
    assert((4,3) in moves)
    assert((5,3) in moves)

def test_king_blocked():
    king = King(4,4)
    moves = king.valid_moves(PiecesContainer([King(4,5)]))

    assert(len(moves) == 7)
    assert((5,4) in moves)
    assert((5,5) in moves)
    assert((4,5) not in moves)
    assert((3,5) in moves)
    assert((3,4) in moves)
    assert((3,3) in moves)
    assert((4,3) in moves)
    assert((5,3) in moves)

def test_king_blocked_enemy():
    king = King(4,4)
    moves = king.valid_moves(PiecesContainer([King(4,5, white=False)]))

    assert(len(moves) == 8)
    assert((5,4) in moves)
    assert((5,5) in moves)
    assert((4,5) in moves)
    assert((3,5) in moves)
    assert((3,4) in moves)
    assert((3,3) in moves)
    assert((4,3) in moves)
    assert((5,3) in moves)