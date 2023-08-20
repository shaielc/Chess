from models.pieces.piece import PiecesContainer
from models.pieces.queen import Queen

def test_queen_moves():
    queen = Queen(4,4)
    moves = queen.valid_moves(PiecesContainer([]))
    assert(len(moves) == 27)
    assert((0,0) in moves)
    assert((7,7) in moves)
    assert((7,1) in moves)
    assert((1,7) in moves)
    assert((0,4) in moves)
    assert((7,4) in moves)
    assert((4,7) in moves)
    assert((4,0) in moves)


def test_queen_blocked():
    queen = Queen(4,4)
    moves = queen.valid_moves(PiecesContainer([Queen(6,4), Queen(6,6)]))
    assert(len(moves) == 23)
    assert((0,0) in moves)
    assert((7,7) not in moves)
    assert((6,6) not in moves)
    assert((7,1) in moves)
    assert((1,7) in moves)
    assert((0,4) in moves)
    assert((7,4) not in moves)
    assert((6,4) not in moves)
    assert((4,7) in moves)
    assert((4,0) in moves)

def test_queen_blocked_enemy():
    queen = Queen(4,4)
    moves = queen.valid_moves(PiecesContainer([Queen(6,4, white=False), Queen(6,6, white=False)]))
    assert(len(moves) == 25)
    assert((0,0) in moves)
    assert((7,7) not in moves)
    assert((6,6) in moves)
    assert((7,1) in moves)
    assert((1,7) in moves)
    assert((0,4) in moves)
    assert((7,4) not in moves)
    assert((6,4) in moves)
    assert((4,7) in moves)
    assert((4,0) in moves)