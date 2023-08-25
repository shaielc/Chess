from models.pieces.piece import PiecesContainer
from models.pieces.bishop import Bishop


def test_bishop_moves():
    bishop = Bishop(4,4)
    moves = bishop.valid_moves(PiecesContainer([]))
    assert(len(moves) == 13)
    assert((0,0) in moves)
    assert((7,7) in moves)
    assert((7,1) in moves)
    assert((1,7) in moves)

def test_bishop_blocked():
    bishop = Bishop(4,4)
    moves = bishop.valid_moves(PiecesContainer([Bishop(2,2, white=False)]))
    assert((2,2) in moves)
    assert((1,1) not in moves)
    assert((0,0) not in moves)
    assert(len(moves) == 11)


    bishop = Bishop(4,4)
    moves = bishop.valid_moves(PiecesContainer([Bishop(2,6)]))
    assert((3,5) in moves)
    assert((2,6) not in moves)
    assert((1,7) not in moves)
    assert(len(moves) == 11)
    

def test_bishop_threatning_empty():
    bishop = Bishop(4,4)
    threats = bishop.threatning(PiecesContainer([]))
    assert(len(threats) == 13)
    assert((0,0) in threats)
    assert((7,7) in threats)
    assert((7,1) in threats)
    assert((1,7) in threats)

def test_bishop_threatning_enemy():
    bishop = Bishop(4,4)
    threats = bishop.threatning(PiecesContainer([Bishop(5,5, white=False)]))
    assert(len(threats) == 11)
    assert((0,0) in threats)
    assert((5,5) in threats)
    assert((6,6) not in threats)
    assert((7,7) not in threats)
    assert((7,1) in threats)
    assert((1,7) in threats)

def test_bishop_defending():
    bishop = Bishop(4,4)
    threats = bishop.threatning(PiecesContainer([Bishop(5,5), Bishop(6,6,white=False)]))
    assert(len(threats) == 11)
    assert((0,0) in threats)
    assert((5,5) in threats)
    assert((6,6) not in threats)
    assert((7,7) not in threats)
    assert((7,1) in threats)
    assert((1,7) in threats)