from models.pieces.piece import PiecesContainer
from models.pieces.rook import Rook
from models.pieces.king import King


# NOTE: another indication of bad design
def test_basic_castling():
    king = King(4,7)
    assert(len(king.can_castle(PiecesContainer([]))) == 0)
    rook = Rook(0,7)
    castles = king.can_castle(PiecesContainer([rook])) 
    assert(len(castles) == 1)
    assert((2,7) in castles)
    king.move(2,7)
    assert(king.x == 2 and king.y == 7)
    assert(rook.x == 3 and rook.y == 7)

def test_king_moved_castling():
    king = King(4,7)
    king.move(3,7)
    king.move(4,7)
    rook = Rook(0,7)
    castles = king.can_castle(PiecesContainer([rook])) 
    assert(len(castles) == 0)
    king.move(2,7)
    assert(king.x == 2 and king.y == 7)
    assert(rook.x == 0 and rook.y == 7)

def test_king_moved_castling():
    king = King(4,7)
    rook = Rook(0,7)
    rook.move(3,7)
    rook.move(0,7)
    castles = king.can_castle(PiecesContainer([rook])) 
    assert(len(castles) == 0)
    king.move(2,7)
    assert(king.x == 2 and king.y == 7)
    assert(rook.x == 0 and rook.y == 7)
